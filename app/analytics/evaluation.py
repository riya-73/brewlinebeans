from __future__ import annotations

from statistics import mean


def smape(actual: list[float], predicted: list[float]) -> float:
    terms = []
    for a, p in zip(actual, predicted):
        denominator = abs(a) + abs(p)
        if denominator:
            terms.append(2 * abs(a - p) / denominator)
    return round(mean(terms), 4) if terms else 0.0


def mae(actual: list[float], predicted: list[float]) -> float:
    return round(mean(abs(a - p) for a, p in zip(actual, predicted)), 4) if actual else 0.0


def rolling_average_predictions(values: list[float], window: int = 7) -> list[float]:
    return [sum(values[max(0, i - window):i]) / len(values[max(0, i - window):i]) if i else values[0] for i in range(len(values))]


def evaluate_baseline(values: list[float], window: int = 7) -> dict:
    if len(values) < 2:
        return {"model": f"moving_average_{window}", "mae": 0, "smape": 0, "n": len(values)}
    actual = values[1:]
    predicted = rolling_average_predictions(values, window)[1:]
    return {"model": f"moving_average_{window}", "mae": mae(actual, predicted), "smape": smape(actual, predicted), "n": len(actual)}


def compare_baselines(values: list[float]) -> list[dict]:
    return [evaluate_baseline(values, window) for window in (3, 7, 14) if len(values) >= 2]
