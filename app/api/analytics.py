from fastapi import APIRouter, Query

from app.analytics.evaluation import compare_baselines
from app.analytics.forecasting import compare_forecasters
from app.analytics.simulation import compare_policies

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.post("/simulate")
def simulate(demand: list[float], initial_stock: float = Query(default=10, ge=0), reorder_point: float = Query(default=5, ge=0), order_quantity: float = Query(default=10, gt=0)) -> list[dict]:
    return compare_policies(demand, initial_stock, reorder_point, order_quantity)


@router.post("/evaluate-baselines")
def evaluate_baselines(values: list[float]) -> list[dict]:
    return compare_baselines(values)


@router.post("/compare-forecasters")
def compare_forecast_models(values: list[float], horizon: int = Query(default=7, ge=1, le=90)) -> dict:
    return compare_forecasters(values, horizon)
