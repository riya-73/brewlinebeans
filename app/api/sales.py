from datetime import UTC, datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import AuditLog, InventoryTransaction, MenuItem, Sale, SaleLine, User
from app.db.session import get_db
from app.schemas_auth_sales import SaleCreate, SaleRead
from app.services.auth import require_roles

router = APIRouter(prefix="/api/sales", tags=["sales"])


@router.post("", response_model=SaleRead, status_code=201)
def create_sale(payload: SaleCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "inventory_operator"))) -> Sale:
    menu_items = {item.id: item for item in db.query(MenuItem).filter(MenuItem.id.in_([line.menu_item_id for line in payload.lines])).all()}
    if len(menu_items) != len({line.menu_item_id for line in payload.lines}):
        raise HTTPException(status_code=404, detail="One or more menu items not found")
    required: dict[int, Decimal] = {}
    total = Decimal("0")
    for line in payload.lines:
        item = menu_items[line.menu_item_id]
        total += Decimal(item.price) * line.quantity
        for recipe in item.recipes:
            required[recipe.ingredient_id] = required.get(recipe.ingredient_id, Decimal("0")) + Decimal(recipe.quantity) * line.quantity
    ingredients = {r.ingredient_id: r.ingredient for item in menu_items.values() for r in item.recipes}
    for ingredient_id, quantity in required.items():
        if Decimal(ingredients[ingredient_id].current_stock) < quantity:
            raise HTTPException(status_code=409, detail=f"Insufficient stock for ingredient {ingredients[ingredient_id].name}")
    sale = Sale(sale_number=f"SALE-{datetime.now(UTC):%Y%m%d%H%M%S%f}", total_amount=total)
    db.add(sale)
    db.flush()
    for line in payload.lines:
        item = menu_items[line.menu_item_id]
        db.add(SaleLine(sale_id=sale.id, menu_item_id=item.id, quantity=line.quantity, unit_price=item.price))
    for ingredient_id, quantity in required.items():
        ingredient = ingredients[ingredient_id]
        ingredient.current_stock -= quantity
        db.add(InventoryTransaction(ingredient_id=ingredient_id, transaction_type="SALE", quantity=quantity, reference=sale.sale_number, reason="Recipe consumption"))
    db.add(AuditLog(actor=user.username, action="CREATE", entity="Sale", entity_id=str(sale.id), details=f"total={total}"))
    db.commit()
    db.refresh(sale)
    return sale


@router.get("", response_model=list[SaleRead])
def list_sales(db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "inventory_operator", "viewer"))) -> list[Sale]:
    return list(db.query(Sale).order_by(Sale.created_at.desc()).limit(100).all())
