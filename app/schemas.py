from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class IngredientBase(BaseModel):
    name: str
    unit: str
    current_stock: Decimal = Field(ge=0)
    reorder_level: Decimal = Field(ge=0)
    shelf_life_days: int = Field(default=7, ge=1)


class IngredientRead(IngredientBase):
    id: int
    status: str
    days_of_cover: float | None = None
    model_config = ConfigDict(from_attributes=True)


class InventoryAdjustment(BaseModel):
    quantity: Decimal
    transaction_type: str = Field(pattern="^(RECEIPT|SALE|WASTE|ADJUSTMENT)$")
    reason: str = Field(min_length=3, max_length=255)
    reference: str | None = None


class SupplierRead(BaseModel):
    id: int
    name: str
    ingredient_id: int
    price_per_unit: Decimal
    lead_time_days: int
    quality_score: Decimal
    reliability: Decimal
    min_order_quantity: Decimal
    model_config = ConfigDict(from_attributes=True)


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    ingredient_id: int
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(gt=0)


class PurchaseOrderRead(PurchaseOrderCreate):
    id: int
    order_number: str
    status: str
    ordered_on: date
    received_quantity: Decimal
    model_config = ConfigDict(from_attributes=True)


class ReceiveOrder(BaseModel):
    quantity: Decimal = Field(gt=0)


class ForecastRead(BaseModel):
    ingredient_id: int
    forecast_date: date
    predicted_quantity: Decimal
    model_name: str
    lower_bound: Decimal | None
    upper_bound: Decimal | None
    model_config = ConfigDict(from_attributes=True)


class SupplierRecommendation(BaseModel):
    supplier_id: int
    supplier_name: str
    score: float
    reasons: list[str]


class HealthRead(BaseModel):
    status: str
    service: str
    timestamp: datetime
