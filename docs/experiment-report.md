# Brewline Beans Experiment Report

## Abstract

This reproducible experiment compares a fixed-threshold inventory policy with a demand-aware dynamic policy for café coffee-bean demand. The data is synthetic, seeded and intended as a methodological demonstration rather than evidence about a real café.

## Research question

Can a demand-aware reorder policy improve service level and reduce stockout exposure compared with a fixed reorder threshold?

## Dataset

- Observations: 365 daily records
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
| Fixed threshold | 0.9305 | 79 | 0.4893 | 402.81 |
| Dynamic forecast | 1.0000 | 0 | 1.4776 | 335.97 |

The dynamic policy changed stockout exposure by approximately **100.0%** relative to the fixed baseline under this synthetic scenario.

### Forecast baseline metrics

| Model | MAE | sMAPE | Observations |
|---|---:|---:|---:|
| moving_average_3 | 0.1639 | 0.1936 | 364 |
| moving_average_7 | 0.1322 | 0.1572 | 364 |
| moving_average_14 | 0.1314 | 0.1566 | 364 |

## Threats to validity

The generator is not a substitute for real point-of-sale data. Cost assumptions, stockout penalties and the dynamic policy parameters can materially change results. A dissertation evaluation should use anonymized operational records, rolling-origin validation, confidence intervals and sensitivity analysis over service factors and cost weights.

## Reproduction

```bash
python -m scripts.generate_experiment_report
python scripts/generate_synthetic.py --days 365 --seed 42
```
