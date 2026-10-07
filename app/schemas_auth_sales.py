from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(default="viewer", pattern="^(manager|inventory_operator|procurement|viewer)$")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class SaleLineCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0, le=1000)


class SaleCreate(BaseModel):
    lines: list[SaleLineCreate] = Field(min_length=1)


class SaleRead(BaseModel):
    id: int
    sale_number: str
    total_amount: Decimal
    created_at: datetime
    model_config = {"from_attributes": True}
