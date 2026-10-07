from contextlib import asynccontextmanager
from datetime import UTC, datetime
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.forecasting import forecast, reorder_recommendation
from app.analytics.suppliers import rank_suppliers
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.sales import router as sales_router
from app.config import get_settings
from app.db.models import (
    AuditLog,
    Ingredient,
    InventoryTransaction,
    MenuItem,
    PurchaseOrder,
    Supplier,
    User,
)
from app.db.session import get_db, init_db
from app.schemas import (
    ForecastRead,
    HealthRead,
    IngredientRead,
    InventoryAdjustment,
    PurchaseOrderCreate,
    PurchaseOrderRead,
    ReceiveOrder,
    SupplierRead,
    SupplierRecommendation,
)
from app.services.auth import require_roles
from app.services.inventory import apply_adjustment, days_of_cover, get_ingredient, stock_status

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", description="Decision-support API for café inventory and procurement.", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router)
app.include_router(sales_router)
app.include_router(analytics_router)


@app.get("/health", response_model=HealthRead, tags=["system"])
def health() -> HealthRead:
    return HealthRead(status="ok", service=settings.app_name, timestamp=datetime.now(UTC))


@app.get("/api/audit", tags=["audit"])
def audit_log(db: Session = Depends(get_db)) -> list[dict]:
    return [{"id": row.id, "actor": row.actor, "action": row.action, "entity": row.entity,
             "entity_id": row.entity_id, "details": row.details, "created_at": row.created_at}
            for row in db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()]


@app.get("/api/menu", tags=["menu"])
def menu(db: Session = Depends(get_db)) -> list[dict]:
    items = db.scalars(select(MenuItem).order_by(MenuItem.category, MenuItem.name)).all()
    return [{"id": i.id, "name": i.name, "category": i.category, "price": i.price, "description": i.description,
             "ingredients": [{"name": r.ingredient.name, "quantity": r.quantity, "unit": r.ingredient.unit} for r in i.recipes]} for i in items]


@app.get("/api/inventory", response_model=list[IngredientRead], tags=["inventory"])
def inventory(status: str | None = Query(default=None), db: Session = Depends(get_db)) -> list[IngredientRead]:
    result = []
    for item in db.scalars(select(Ingredient).order_by(Ingredient.name)).all():
        item_status = stock_status(item)
        if status and item_status.lower() != status.lower():
            continue
        result.append(IngredientRead.model_validate({**item.__dict__, "status": item_status, "days_of_cover": days_of_cover(item)}))
    return result


@app.post("/api/inventory/{ingredient_id}/transactions", response_model=IngredientRead, tags=["inventory"])
def inventory_transaction(ingredient_id: int, payload: InventoryAdjustment, db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "inventory_operator"))) -> IngredientRead:
    item = apply_adjustment(db, get_ingredient(db, ingredient_id), payload.quantity, payload.transaction_type, payload.reason, payload.reference)
    db.add(AuditLog(actor=user.username, action="ADJUST_STOCK", entity="Ingredient", entity_id=str(ingredient_id), details=payload.reason))
    db.commit()
    return IngredientRead.model_validate({**item.__dict__, "status": stock_status(item), "days_of_cover": days_of_cover(item)})


@app.get("/api/suppliers", response_model=list[SupplierRead], tags=["suppliers"])
def suppliers(ingredient_id: int | None = None, db: Session = Depends(get_db)) -> list[SupplierRead]:
    query = select(Supplier).order_by(Supplier.name)
    if ingredient_id:
        query = query.where(Supplier.ingredient_id == ingredient_id)
    return list(db.scalars(query).all())


@app.get("/api/suppliers/{ingredient_id}/recommendations", response_model=list[SupplierRecommendation], tags=["suppliers"])
def supplier_recommendations(ingredient_id: int, db: Session = Depends(get_db)) -> list[SupplierRecommendation]:
    rows = db.scalars(select(Supplier).where(Supplier.ingredient_id == ingredient_id)).all()
    return rank_suppliers(rows)


@app.get("/api/purchases", response_model=list[PurchaseOrderRead], tags=["purchases"])
def purchases(db: Session = Depends(get_db)) -> list[PurchaseOrderRead]:
    return list(db.scalars(select(PurchaseOrder).order_by(PurchaseOrder.ordered_on.desc())).all())


@app.post("/api/purchases", response_model=PurchaseOrderRead, status_code=201, tags=["purchases"])
def create_purchase(payload: PurchaseOrderCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "procurement"))) -> PurchaseOrder:
    if not db.get(Supplier, payload.supplier_id) or not db.get(Ingredient, payload.ingredient_id):
        raise HTTPException(status_code=404, detail="Supplier or ingredient not found")
    order = PurchaseOrder(order_number=f"PO-{datetime.now(UTC):%Y%m%d%H%M%S%f}", **payload.model_dump())
    db.add(order)
    db.add(AuditLog(actor=user.username, action="CREATE", entity="PurchaseOrder", details=f"ingredient={payload.ingredient_id}"))
    db.commit()
    db.refresh(order)
    return order


@app.post("/api/purchases/{purchase_id}/receive", response_model=PurchaseOrderRead, tags=["purchases"])
def receive_purchase(purchase_id: int, payload: ReceiveOrder, db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "procurement", "inventory_operator"))) -> PurchaseOrder:
    order = db.get(PurchaseOrder, purchase_id)
    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    remaining = Decimal(order.quantity) - Decimal(order.received_quantity)
    if payload.quantity > remaining:
        raise HTTPException(status_code=409, detail="Received quantity exceeds remaining order quantity")
    item = get_ingredient(db, order.ingredient_id)
    order.received_quantity += payload.quantity
    order.status = "RECEIVED" if order.received_quantity == order.quantity else "PARTIALLY_RECEIVED"
    item.current_stock += payload.quantity
    db.add(InventoryTransaction(ingredient_id=item.id, transaction_type="RECEIPT", quantity=payload.quantity, reference=order.order_number, reason="Purchase order receipt"))
    db.add(AuditLog(actor=user.username, action="RECEIVE", entity="PurchaseOrder", entity_id=str(order.id), details=f"quantity={payload.quantity}"))
    db.commit()
    db.refresh(order)
    return order


@app.get("/api/analytics/reorder/{ingredient_id}", tags=["analytics"])
def reorder(ingredient_id: int, daily_demand: float = Query(default=1, gt=0), lead_time_days: int = Query(default=2, ge=1), db: Session = Depends(get_db)) -> dict:
    item = get_ingredient(db, ingredient_id)
    return {"ingredient_id": ingredient_id, "ingredient_name": item.name, **reorder_recommendation(Decimal(item.current_stock), Decimal(item.reorder_level), daily_demand, lead_time_days)}


@app.post("/api/analytics/forecast", response_model=list[ForecastRead], tags=["analytics"])
def generate_forecast(ingredient_id: int, values: list[float], horizon: int = Query(default=7, ge=1, le=90), db: Session = Depends(get_db)) -> list[ForecastRead]:
    get_ingredient(db, ingredient_id)
    return [ForecastRead.model_validate({"ingredient_id": ingredient_id, **row}) for row in forecast(values, horizon)]
