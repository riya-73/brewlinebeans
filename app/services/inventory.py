from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ingredient, InventoryTransaction


def stock_status(item: Ingredient) -> str:
    if item.current_stock < item.reorder_level * Decimal("0.6"):
        return "Critical"
    if item.current_stock < item.reorder_level:
        return "Low Stock"
    return "Healthy"


def days_of_cover(item: Ingredient, daily_demand: Decimal = Decimal("1")) -> float:
    if daily_demand <= 0:
        return float("inf")
    return round(float(item.current_stock / daily_demand), 2)


def apply_adjustment(db: Session, item: Ingredient, quantity: Decimal, transaction_type: str, reason: str, reference: str | None = None) -> Ingredient:
    if transaction_type in {"SALE", "WASTE"} and quantity > item.current_stock:
        raise HTTPException(status_code=409, detail="Insufficient stock for this transaction")
    delta = quantity if transaction_type in {"RECEIPT", "ADJUSTMENT"} else -quantity
    item.current_stock += delta
    db.add(InventoryTransaction(ingredient_id=item.id, transaction_type=transaction_type, quantity=quantity, reason=reason, reference=reference))
    db.commit()
    db.refresh(item)
    return item


def get_ingredient(db: Session, ingredient_id: int) -> Ingredient:
    item = db.scalar(select(Ingredient).where(Ingredient.id == ingredient_id))
    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return item
