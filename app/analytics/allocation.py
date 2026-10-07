from decimal import Decimal


def allocate_budget(demands: list, supplier_map: dict[int, list], ingredients: dict[int, object], budget: Decimal) -> dict:
    lines = []
    warnings = []
    # Allocate higher-risk ingredients first, then choose the best feasible supplier.
    ordered = sorted(demands, key=lambda item: item.quantity, reverse=True)
    total = Decimal("0")
    for demand in ordered:
        options = sorted(supplier_map.get(demand.ingredient_id, []), key=lambda s: (float(s.price_per_unit), -float(s.reliability)))
        if not options:
            warnings.append(f"No supplier found for ingredient {demand.ingredient_id}.")
            continue
        feasible = [s for s in options if total + Decimal(demand.quantity) * Decimal(s.price_per_unit) <= budget]
        supplier = feasible[0] if feasible else options[0]
        cost = Decimal(demand.quantity) * Decimal(supplier.price_per_unit)
        if total + cost > budget:
            warnings.append(f"Budget cannot cover requested {demand.quantity} units of {ingredients[demand.ingredient_id].name}.")
            continue
        total += cost
        lines.append({"ingredient_id": demand.ingredient_id, "ingredient_name": ingredients[demand.ingredient_id].name, "supplier_id": supplier.id, "supplier_name": supplier.name, "quantity": demand.quantity, "unit_price": supplier.price_per_unit, "line_cost": cost, "score": round(float(supplier.reliability) / 100 * 0.4 + float(supplier.quality_score) / 10 * 0.35 + (1 / max(supplier.lead_time_days, 1)) * 0.25, 4)})
    return {"budget": budget, "total_cost": total, "remaining_budget": budget - total, "feasible": not warnings and len(lines) == len(demands), "lines": lines, "warnings": warnings}
