# Data Dictionary

| Entity | Field | Meaning | Unit / values |
|---|---|---|---|
| Ingredient | `current_stock` | Current operational balance | Ingredient-specific unit |
| Ingredient | `reorder_level` | Existing operational threshold | Ingredient-specific unit |
| Ingredient | `shelf_life_days` | Expected usable life | Days |
| RecipeIngredient | `quantity` | Amount consumed per menu item | Ingredient-specific unit |
| InventoryTransaction | `transaction_type` | Stock movement category | `RECEIPT`, `SALE`, `WASTE`, `ADJUSTMENT` |
| InventoryTransaction | `quantity` | Absolute movement amount | Ingredient-specific unit |
| Supplier | `price_per_unit` | Quoted supplier price | INR per ingredient unit |
| Supplier | `lead_time_days` | Expected delivery time | Days |
| Supplier | `quality_score` | Quality assessment | 0–10 |
| Supplier | `reliability` | On-time/reliable delivery measure | 0–100% |
| PurchaseOrder | `status` | Procurement lifecycle state | `DRAFT`, `PARTIALLY_RECEIVED`, `RECEIVED`, `CANCELLED` |
| Forecast | `predicted_quantity` | Predicted future demand | Ingredient-specific unit |

## Provenance

The initial seed data is synthetic and derived from the original front-end demonstration values. It must not be described as real café operational data. For the dissertation, replace or augment it with anonymized real records or a documented synthetic-data generator.

## Analytical cautions

- Do not calculate MAPE when actual demand is zero without a defined convention.
- Use time-based splits for forecasting evaluation.
- Record all model names, parameters, data windows and random seeds.
- Keep prices and stock units consistent; do not compare kilograms, litres and pieces directly without normalization.
