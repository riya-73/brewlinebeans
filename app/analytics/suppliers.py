from __future__ import annotations


def rank_suppliers(suppliers: list, weights: dict[str, float] | None = None) -> list[dict]:
    if not suppliers:
        return []
    weights = weights or {"price": 0.35, "lead_time": 0.2, "quality": 0.2, "reliability": 0.25}
    prices = [float(s.price_per_unit) for s in suppliers]
    leads = [float(s.lead_time_days) for s in suppliers]
    qualities = [float(s.quality_score) for s in suppliers]
    reliabilities = [float(s.reliability) for s in suppliers]

    def benefit(value: float, values: list[float]) -> float:
        span = max(values) - min(values)
        return 1.0 if span == 0 else (value - min(values)) / span

    def cost(value: float, values: list[float]) -> float:
        span = max(values) - min(values)
        return 1.0 if span == 0 else (max(values) - value) / span

    ranked = []
    for s in suppliers:
        score = (weights["price"] * cost(float(s.price_per_unit), prices) +
                 weights["lead_time"] * cost(float(s.lead_time_days), leads) +
                 weights["quality"] * benefit(float(s.quality_score), qualities) +
                 weights["reliability"] * benefit(float(s.reliability), reliabilities))
        ranked.append({"supplier_id": s.id, "supplier_name": s.name, "score": round(score, 4),
                       "reasons": ["price", "lead time", "quality", "reliability"]})
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
