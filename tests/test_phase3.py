from datetime import date, timedelta
from decimal import Decimal

from app.analytics.allocation import allocate_budget
from app.db.models import Ingredient, InventoryBatch
from app.db.session import SessionLocal, init_db
from app.services.operations import consume_batches


def test_budget_allocation_reports_infeasible_demand():
    ingredient = Ingredient(id=1, name="Beans", unit="kg")
    supplier = type("SupplierStub", (), {"id": 1, "name": "Supplier", "price_per_unit": Decimal("100"), "reliability": Decimal("95"), "quality_score": Decimal("9"), "lead_time_days": 2})()
    result = allocate_budget([type("Demand", (), {"ingredient_id": 1, "quantity": Decimal("20")})()], {1: [supplier]}, {1: ingredient}, Decimal("100"))
    assert result["feasible"] is False
    assert result["lines"] == []


def test_fefo_consumes_earliest_expiry_first():
    init_db()
    with SessionLocal() as db:
        ingredient = Ingredient(name="Test FEFO", unit="kg", current_stock=5, reorder_level=1)
        db.add(ingredient)
        db.flush()
        late = InventoryBatch(ingredient_id=ingredient.id, lot_number="LATE", quantity=3, expires_on=date.today() + timedelta(days=10))
        early = InventoryBatch(ingredient_id=ingredient.id, lot_number="EARLY", quantity=2, expires_on=date.today() + timedelta(days=2))
        db.add_all([late, early])
        db.flush()
        consumed = consume_batches(db, ingredient.id, Decimal("2.5"))
        assert [batch.lot_number for batch in consumed] == ["EARLY", "LATE"]
        db.rollback()
