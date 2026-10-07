from decimal import Decimal

from fastapi.testclient import TestClient

from app.analytics.forecasting import reorder_recommendation
from app.analytics.suppliers import rank_suppliers
from app.db.models import Supplier
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_reorder_recommendation_is_deterministic():
    result = reorder_recommendation(Decimal("4"), Decimal("10"), 2.0, 3)
    assert result["should_order"] is True
    assert result["recommended_quantity"] > 0


def test_supplier_ranking_prefers_balanced_supplier():
    suppliers = [
        Supplier(id=1, name="Cheap", price_per_unit=10, lead_time_days=8, quality_score=7, reliability=80),
        Supplier(id=2, name="Balanced", price_per_unit=12, lead_time_days=2, quality_score=9, reliability=98),
    ]
    results = rank_suppliers(suppliers)
    assert results[0]["supplier_name"] == "Balanced"
