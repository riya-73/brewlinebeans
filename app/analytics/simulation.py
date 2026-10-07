from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationResult:
    policy: str
    service_level: float
    stockout_days: int
    average_inventory: float
    total_cost: float


def simulate_policy(demand: list[float], initial_stock: float, reorder_point: float, order_quantity: float, unit_cost: float = 1.0, holding_cost: float = 0.05, shortage_cost: float = 5.0, policy: str = "fixed_threshold") -> SimulationResult:
    stock = initial_stock
    inventory_sum = 0.0
    stockout_days = 0
    total_cost = 0.0
    served = 0.0
    requested = sum(max(x, 0) for x in demand)
    for day_demand in demand:
        if stock < reorder_point:
            stock += order_quantity
            total_cost += order_quantity * unit_cost
        fulfilled = min(stock, max(day_demand, 0))
        stock -= fulfilled
        if fulfilled < day_demand:
            stockout_days += 1
            total_cost += (day_demand - fulfilled) * shortage_cost
        served += fulfilled
        inventory_sum += stock
        total_cost += stock * holding_cost
    return SimulationResult(policy=policy, service_level=round(served / requested, 4) if requested else 1.0,
                             stockout_days=stockout_days, average_inventory=round(inventory_sum / len(demand), 4) if demand else 0,
                             total_cost=round(total_cost, 2))


def compare_policies(demand: list[float], initial_stock: float, reorder_point: float, order_quantity: float) -> list[dict]:
    baseline = simulate_policy(demand, initial_stock, reorder_point, order_quantity, policy="fixed_threshold")
    dynamic_point = max(reorder_point, sum(demand[-7:]) / min(7, len(demand)) * 2) if demand else reorder_point
    dynamic = simulate_policy(demand, initial_stock, dynamic_point, order_quantity, policy="dynamic_forecast")
    return [baseline.__dict__, dynamic.__dict__]
