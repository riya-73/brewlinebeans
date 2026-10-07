from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from statistics import mean, pstdev


def moving_average(values: list[float], window: int = 7) -> float:
    if not values:
        return 0.0
    sample = values[-window:]
    return round(mean(sample), 4)


def forecast(values: list[float], horizon: int = 7, window: int = 7) -> list[dict]:
    baseline = moving_average(values, window)
    uncertainty = pstdev(values[-window:]) if len(values) > 1 else baseline * 0.2
    today = date.today()
    return [
        {"forecast_date": today + timedelta(days=i + 1), "predicted_quantity": Decimal(str(round(max(baseline, 0), 3))),
         "lower_bound": Decimal(str(round(max(baseline - uncertainty, 0), 3))),
         "upper_bound": Decimal(str(round(baseline + uncertainty, 3))), "model_name": f"moving_average_{window}"}
        for i in range(horizon)
    ]


def reorder_recommendation(current_stock: Decimal, reorder_level: Decimal, daily_demand: float, lead_time_days: int, service_factor: float = 1.65) -> dict:
    demand_during_lead = max(daily_demand, 0) * lead_time_days
    safety_stock = service_factor * max(daily_demand, 0) ** 0.5
    reorder_point = demand_during_lead + safety_stock
    order_quantity = max(0.0, reorder_point * 2 - float(current_stock))
    return {"reorder_point": round(reorder_point, 3), "safety_stock": round(safety_stock, 3), "recommended_quantity": round(order_quantity, 3), "should_order": float(current_stock) <= reorder_point}


def holt_winters_forecast(values: list[float], horizon: int = 7, seasonal_periods: int = 7) -> list[float]:
    """Forecast with additive Holt-Winters when enough observations exist."""
    if len(values) < max(2 * seasonal_periods, 14):
        return [round(moving_average(values, min(seasonal_periods, len(values))), 4)] * horizon
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    model = ExponentialSmoothing(values, trend="add", seasonal="add", seasonal_periods=seasonal_periods, initialization_method="estimated")
    return [round(max(float(value), 0), 4) for value in model.fit(optimized=True).forecast(horizon)]


def compare_forecasters(values: list[float], horizon: int = 7) -> dict:
    return {"moving_average": [float(row["predicted_quantity"]) for row in forecast(values, horizon)],
            "holt_winters": holt_winters_forecast(values, horizon)}
