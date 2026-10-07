from pathlib import Path

from app.analytics.evaluation import compare_baselines
from app.analytics.simulation import compare_policies
from scripts.generate_synthetic import generate


def main() -> None:
    rows = generate(365, 42)
    demand = [row["demand_kg"] for row in rows]
    policies = compare_policies(demand, initial_stock=1.0, reorder_point=0.5, order_quantity=1.5)
    metrics = compare_baselines(demand)
    baseline, dynamic = policies
    reduction = round((baseline["stockout_days"] - dynamic["stockout_days"]) / max(baseline["stockout_days"], 1) * 100, 2)
    metric_rows = "\n".join(
        f"| {row['model']} | {row['mae']:.4f} | {row['smape']:.4f} | {row['n']} |" for row in metrics
    )
    report = f"""# Brewline Beans Experiment Report

## Abstract

This reproducible experiment compares a fixed-threshold inventory policy with a demand-aware dynamic policy for café coffee-bean demand. The data is synthetic, seeded and intended as a methodological demonstration rather than evidence about a real café.

## Research question

Can a demand-aware reorder policy improve service level and reduce stockout exposure compared with a fixed reorder threshold?

## Dataset

- Observations: {len(rows)} daily records
- Ingredient: Coffee Beans
- Generator seed: 42
- Features: weekday effect, annual seasonality, promotion spikes and Gaussian noise
- Demand unit: kg

## Methodology

The fixed policy reorders when stock is below 0.5 kg and orders 1.5 kg. The dynamic policy raises the reorder point using the recent seven-day demand average. Both policies use identical starting stock, order quantity, unit cost, holding cost and shortage cost.

Forecast baselines were evaluated with rolling one-step predictions using moving-average windows of 3, 7 and 14 days.

## Results

| Policy | Service level | Stockout days | Average inventory | Total cost |
|---|---:|---:|---:|---:|
| Fixed threshold | {baseline['service_level']:.4f} | {baseline['stockout_days']} | {baseline['average_inventory']:.4f} | {baseline['total_cost']:.2f} |
| Dynamic forecast | {dynamic['service_level']:.4f} | {dynamic['stockout_days']} | {dynamic['average_inventory']:.4f} | {dynamic['total_cost']:.2f} |

The dynamic policy changed stockout exposure by approximately **{reduction}%** relative to the fixed baseline under this synthetic scenario.

### Forecast baseline metrics

| Model | MAE | sMAPE | Observations |
|---|---:|---:|---:|
{metric_rows}

## Threats to validity

The generator is not a substitute for real point-of-sale data. Cost assumptions, stockout penalties and the dynamic policy parameters can materially change results. A dissertation evaluation should use anonymized operational records, rolling-origin validation, confidence intervals and sensitivity analysis over service factors and cost weights.

## Reproduction

```bash
python -m scripts.generate_experiment_report
python scripts/generate_synthetic.py --days 365 --seed 42
```
"""
    Path("docs/experiment-report.md").write_text(report, encoding="utf-8")
    print("Wrote docs/experiment-report.md")


if __name__ == "__main__":
    main()
