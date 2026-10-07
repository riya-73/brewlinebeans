from datetime import date, timedelta
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ingredient, InventoryBatch, Notification


def consume_batches(db: Session, ingredient_id: int, quantity: Decimal) -> list[InventoryBatch]:
    remaining = quantity
    batches = db.scalars(select(InventoryBatch).where(InventoryBatch.ingredient_id == ingredient_id, InventoryBatch.status == "ACTIVE", InventoryBatch.quantity > 0).order_by(InventoryBatch.expires_on)).all()
    if sum((Decimal(batch.quantity) for batch in batches), Decimal("0")) < quantity:
        raise HTTPException(status_code=409, detail="Insufficient non-expired batch stock")
    consumed = []
    for batch in batches:
        if remaining <= 0:
            break
        used = min(Decimal(batch.quantity), remaining)
        batch.quantity -= used
        remaining -= used
        if batch.quantity == 0:
            batch.status = "DEPLETED"
        consumed.append(batch)
    return consumed


def run_alert_scan(db: Session, expiry_window_days: int = 3) -> list[Notification]:
    today = date.today()
    cutoff = today + timedelta(days=expiry_window_days)
    created: list[Notification] = []
    for item in db.scalars(select(Ingredient)).all():
        if item.current_stock < item.reorder_level:
            message = f"{item.name} is below reorder level ({item.current_stock} {item.unit} remaining)."
            exists = db.scalar(select(Notification).where(Notification.notification_type == "LOW_STOCK", Notification.ingredient_id == item.id, Notification.is_read.is_(False)))
            if not exists:
                created.append(Notification(notification_type="LOW_STOCK", severity="CRITICAL" if item.current_stock < item.reorder_level * Decimal("0.6") else "WARNING", message=message, ingredient_id=item.id))
    for batch in db.scalars(select(InventoryBatch).where(InventoryBatch.status == "ACTIVE", InventoryBatch.quantity > 0, InventoryBatch.expires_on <= cutoff)).all():
        kind = "EXPIRED" if batch.expires_on < today else "EXPIRING_SOON"
        exists = db.scalar(select(Notification).where(Notification.notification_type == kind, Notification.batch_id == batch.id, Notification.is_read.is_(False)))
        if not exists:
            created.append(Notification(notification_type=kind, severity="CRITICAL" if kind == "EXPIRED" else "WARNING", message=f"Batch {batch.lot_number} expires on {batch.expires_on} with {batch.quantity} units remaining.", ingredient_id=batch.ingredient_id, batch_id=batch.id))
    db.add_all(created)
    db.commit()
    return created
