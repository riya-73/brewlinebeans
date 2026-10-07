from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BatchCreate(BaseModel):
    ingredient_id: int
    lot_number: str = Field(min_length=2, max_length=80)
    quantity: Decimal = Field(gt=0)
    received_on: date = Field(default_factory=date.today)
    expires_on: date


class BatchRead(BatchCreate):
    id: int
    status: str
    model_config = {"from_attributes": True}


class NotificationRead(BaseModel):
    id: int
    notification_type: str
    severity: str
    message: str
    ingredient_id: int | None
    batch_id: int | None
    is_read: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class AllocationDemand(BaseModel):
    ingredient_id: int
    quantity: Decimal = Field(gt=0)


class AllocationRequest(BaseModel):
    demands: list[AllocationDemand] = Field(min_length=1)
    budget: Decimal = Field(gt=0)


class AllocationLine(BaseModel):
    ingredient_id: int
    ingredient_name: str
    supplier_id: int
    supplier_name: str
    quantity: Decimal
    unit_price: Decimal
    line_cost: Decimal
    score: float


class AllocationResponse(BaseModel):
    budget: Decimal
    total_cost: Decimal
    remaining_budget: Decimal
    feasible: bool
    lines: list[AllocationLine]
    warnings: list[str]
