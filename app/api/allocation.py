from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.allocation import allocate_budget
from app.db.models import AuditLog, Ingredient, Supplier, User
from app.db.session import get_db
from app.schemas_operations import AllocationRequest, AllocationResponse
from app.services.auth import require_roles

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.post("/allocate", response_model=AllocationResponse)
def allocate(payload: AllocationRequest, db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "procurement"))) -> dict:
    ids = [d.ingredient_id for d in payload.demands]
    ingredients = {item.id: item for item in db.scalars(select(Ingredient).where(Ingredient.id.in_(ids))).all()}
    supplier_map = {}
    for ingredient_id in ids:
        supplier_map[ingredient_id] = list(db.scalars(select(Supplier).where(Supplier.ingredient_id == ingredient_id)).all())
    result = allocate_budget(payload.demands, supplier_map, ingredients, payload.budget)
    db.add(AuditLog(actor=user.username, action="ALLOCATE_BUDGET", entity="SupplierAllocation", details=f"budget={payload.budget}, total={result['total_cost']}"))
    db.commit()
    return result
