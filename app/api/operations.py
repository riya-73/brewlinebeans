from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AuditLog, InventoryBatch, Notification, User
from app.db.session import get_db
from app.schemas_operations import BatchCreate, BatchRead, NotificationRead
from app.services.auth import require_roles
from app.services.operations import run_alert_scan

router = APIRouter(prefix="/api/operations", tags=["operations"])


@router.get("/batches", response_model=list[BatchRead])
def list_batches(ingredient_id: int | None = None, include_depleted: bool = False, db: Session = Depends(get_db)) -> list[InventoryBatch]:
    query = select(InventoryBatch).order_by(InventoryBatch.expires_on)
    if ingredient_id:
        query = query.where(InventoryBatch.ingredient_id == ingredient_id)
    if not include_depleted:
        query = query.where(InventoryBatch.status == "ACTIVE")
    return list(db.scalars(query).all())


@router.post("/batches", response_model=BatchRead, status_code=201)
def create_batch(payload: BatchCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "procurement", "inventory_operator"))) -> InventoryBatch:
    if payload.expires_on < payload.received_on:
        raise HTTPException(status_code=422, detail="Expiry date must not precede received date")
    batch = InventoryBatch(**payload.model_dump())
    db.add(batch)
    db.add(AuditLog(actor=user.username, action="CREATE", entity="InventoryBatch", details=f"lot={payload.lot_number}"))
    db.commit()
    db.refresh(batch)
    return batch


@router.get("/alerts", response_model=list[NotificationRead])
def list_alerts(unread_only: bool = Query(default=False), db: Session = Depends(get_db)) -> list[Notification]:
    query = select(Notification).order_by(Notification.created_at.desc())
    if unread_only:
        query = query.where(Notification.is_read.is_(False))
    return list(db.scalars(query.limit(200)).all())


@router.post("/alerts/scan", response_model=list[NotificationRead])
def scan_alerts(expiry_window_days: int = Query(default=3, ge=0, le=30), db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "inventory_operator"))) -> list[Notification]:
    created = run_alert_scan(db, expiry_window_days)
    if created:
        db.add(AuditLog(actor=user.username, action="SCAN_ALERTS", entity="Notification", details=f"created={len(created)}"))
        db.commit()
    return created


@router.post("/alerts/{notification_id}/read", response_model=NotificationRead)
def mark_read(notification_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("manager", "inventory_operator", "procurement", "viewer"))) -> Notification:
    notification = db.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.is_read = True
    db.add(AuditLog(actor=user.username, action="READ", entity="Notification", entity_id=str(notification_id)))
    db.commit()
    db.refresh(notification)
    return notification
