import argparse
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path


def generate(days: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    start = date(2025, 1, 1)
    rows = []
    for offset in range(days):
        day = start + timedelta(days=offset)
        weekend_effect = 1.35 if day.weekday() >= 5 else 1.0
        seasonal_effect = 1 + 0.18 * math.sin(2 * math.pi * offset / 365)
        promotion = 1.25 if offset % 29 == 0 else 1.0
        demand = max(0, round(rng.gauss(42 * weekend_effect * seasonal_effect * promotion, 5)))
        rows.append({"date": day.isoformat(), "ingredient": "Coffee Beans", "demand_kg": round(demand * 0.018, 3), "promotion": int(promotion > 1)})
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate reproducible Brewline demand data")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("data/synthetic/demand.csv"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "ingredient", "demand_kg", "promotion"])
        writer.writeheader()
        writer.writerows(generate(args.days, args.seed))
    print(f"Generated {args.days} rows at {args.output} with seed {args.seed}")
