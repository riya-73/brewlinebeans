# Brewline Beans: Master’s-Level Python Project Roadmap

## 1. Current assessment

The current repository is a good UI prototype for a café supply-chain portal, but it is not yet a Python project:

- Five static HTML pages: menu, inventory, suppliers, purchases and analytics.
- Data is hard-coded in `data.js`.
- Business logic runs in the browser through JavaScript.
- Inventory, supplier and purchase values are sample data rather than persistent records.
- Analytics are descriptive charts, not predictive or decision-support analytics.
- There is no authentication, role-based access, audit trail, API, database, automated testing or deployment pipeline.
- The current README is only a one-line description.

The strongest academic direction is therefore:

> **An intelligent café inventory and supplier decision-support system that combines demand forecasting, inventory optimization and multi-criteria supplier selection.**

This gives you a clear software-engineering product plus a research contribution that can be evaluated quantitatively.

---

## 2. Recommended project title

### Primary title

**Brewline: A Predictive Inventory and Supplier Optimization Platform for Café Supply Chains**

### Possible research question

> Can a demand-aware inventory and supplier decision-support system reduce stockout risk and procurement cost compared with static reorder thresholds and manual supplier selection?

### Supporting questions

1. How accurately can ingredient demand be forecast from historical sales and contextual variables?
2. Which inventory policy gives the best trade-off between holding cost, stockout risk and service level?
3. Can a multi-criteria supplier ranking model improve procurement decisions compared with selecting the cheapest supplier?
4. How much operational improvement is obtained compared with the current rule-based baseline?

---

## 3. Target Python architecture

Use a modular monorepo rather than converting the HTML files into a single Python script.

```text
brewlinebeans/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment-based settings
│   ├── db/
│   │   ├── session.py
│   │   ├── models.py           # SQLAlchemy models
│   │   └── migrations/
│   ├── api/
│   │   ├── auth.py
│   │   ├── menu.py
│   │   ├── inventory.py
│   │   ├── suppliers.py
│   │   ├── purchases.py
│   │   ├── forecasts.py
│   │   └── optimization.py
│   ├── schemas/                # Pydantic request/response models
│   ├── services/               # Business rules and domain services
│   ├── analytics/              # Forecasting, KPIs and evaluation
│   └── templates/              # Optional Jinja templates
├── frontend/                   # Existing UI migrated to React or kept as static client
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
├── notebooks/                  # Exploratory analysis only
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
├── scripts/                    # Import, seed, train and evaluation scripts
├── docs/
│   ├── architecture.md
│   ├── data-dictionary.md
│   └── api.md
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── README.md
└── LICENSE
```

### Suggested technology stack

| Layer | Recommendation | Purpose |
|---|---|---|
| API | FastAPI | Typed, documented REST API and automatic OpenAPI docs |
| ORM | SQLAlchemy 2 + Alembic | Database models and migrations |
| Validation | Pydantic v2 | Request and response validation |
| Database | PostgreSQL | Production-grade persistence; SQLite for quick local tests |
| Front end | React/TypeScript or current HTML/JS | Reuse the existing design while replacing data.js calls with API calls |
| Data analysis | pandas, NumPy | Cleaning, transformation and exploratory analysis |
| Forecasting | statsmodels + scikit-learn; optionally LightGBM/XGBoost | Baselines and predictive models |
| Optimization | scipy.optimize or OR-Tools | Reorder and supplier allocation optimization |
| Charts | Plotly or existing Chart.js | Interactive dashboards |
| Testing | pytest, pytest-cov, httpx | Unit, integration and API tests |
| Quality | Ruff, mypy, pre-commit | Formatting, linting and type checking |
| Deployment | Docker Compose | Reproducible development and deployment |

Avoid using machine learning only for appearance. Every model should support a measurable operational decision.

---

## 4. Core modules to build

### A. Authentication and roles

Add users and role-based permissions:

- **Manager:** all data, reports and configuration.
- **Inventory operator:** stock updates, purchase receipts and stock adjustments.
- **Procurement officer:** suppliers, purchase orders and supplier comparisons.
- **Staff/viewer:** menu and read-only operational information.

Implement password hashing, JWT or secure session authentication, route authorization and an audit log for important changes.

### B. Persistent data model

Recommended entities:

- `User`
- `Role`
- `MenuItem`
- `Ingredient`
- `RecipeIngredient`
- `InventorySnapshot`
- `InventoryTransaction`
- `Supplier`
- `SupplierIngredient`
- `PurchaseOrder`
- `PurchaseOrderLine`
- `Sale`
- `SaleLine`
- `Forecast`
- `ReorderRecommendation`
- `AuditEvent`

Important design improvement: replace the current single `currentStock` value with an inventory transaction ledger. Stock should be derived from receipts, sales/consumption, waste, corrections and transfers. This makes the system auditable and academically defensible.

### C. Menu-to-inventory consumption

The current `menuItems` already contain ingredient quantities. Convert that into a normalized recipe model:

```text
MenuItem ──< RecipeIngredient >── Ingredient
```

When a sale is recorded, deduct the recipe quantities from inventory. This creates a meaningful connection between the menu, sales demand and stock levels.

Include waste and spoilage as separate transaction types so that the system can calculate:

- Theoretical consumption.
- Actual consumption.
- Variance and waste percentage.
- Estimated cost of waste.

### D. Purchase-order workflow

Add a complete procurement workflow:

1. Generate recommendation from forecast and inventory position.
2. Select supplier or supplier combination.
3. Create draft purchase order.
4. Approve purchase order.
5. Receive partial or full delivery.
6. Record quality issues and price variance.
7. Update inventory through a receipt transaction.

Use explicit statuses such as `DRAFT`, `APPROVED`, `PARTIALLY_RECEIVED`, `RECEIVED`, `CANCELLED`.

---

## 5. The research contribution: analytics and optimization

### A. Establish a non-ML baseline first

The baseline is essential for a master’s project. Implement:

- Current stock below reorder level.
- Fixed reorder quantity.
- Moving-average demand.
- Manual supplier choice based on lowest unit price.

All advanced models must be compared against this baseline.

### B. Demand forecasting

Start with one model per ingredient or ingredient family. Compare:

1. Seasonal naïve forecast.
2. Moving average.
3. Exponential smoothing / Holt-Winters.
4. SARIMA where sufficient time-series data exists.
5. Gradient-boosted regression with lag, weekday, month, holiday and promotion features.

Potential features:

- Historical daily quantity sold.
- Day of week and month.
- Public holiday flag.
- Weather or temperature, if available and ethically sourced.
- Promotions and price changes.
- Weekends and local events.
- Ingredient shelf life.

Use time-series cross-validation, not random train/test splitting.

Recommended metrics:

- MAE.
- RMSE.
- MAPE or sMAPE, with care for zero-demand periods.
- WAPE for aggregate operational demand.
- Forecast bias.

Example research output:

> Holt-Winters reduced WAPE by X% compared with the moving-average baseline for high-volume ingredients.

Do not claim this until it is supported by your experiment results.

### C. Inventory optimization

For each ingredient calculate:

- Demand during lead time.
- Safety stock.
- Reorder point.
- Economic order quantity, where assumptions are valid.
- Days of inventory remaining.
- Stockout probability.
- Expected holding cost.
- Expected shortage cost.
- Shelf-life risk.

A useful policy is:

```text
reorder_point = expected_lead_time_demand + safety_stock
order_quantity = optimization_policy(forecast, inventory_position, supplier_constraints)
```

Use a simulation engine to compare policies over historical or synthetically generated demand. Measure service level and cost, rather than only displaying a chart.

### D. Supplier selection

Turn the existing `qualityScore`, `reliability`, price and lead time into a transparent multi-criteria decision model.

Possible approach:

1. Normalize price, lead time, quality and reliability.
2. Assign weights using AHP, entropy weighting or a justified managerial weighting scheme.
3. Rank suppliers using TOPSIS or a weighted scoring model.
4. Run sensitivity analysis on the weights.
5. Compare against the cheapest-supplier baseline.

Example criteria:

- Unit price: minimize.
- Lead time: minimize.
- Quality score: maximize.
- Reliability: maximize.
- Minimum order quantity: minimize or satisfy constraint.
- Sustainability score: maximize, if data is available.

A stronger extension is a constrained supplier-allocation problem that considers budget, capacity, minimum order quantities and service-level requirements.

### E. Explainable recommendations

Every recommendation should state why it was produced:

> Order 18 kg of coffee beans from Highland Roasters because projected 14-day demand is 11.8 kg, current inventory position is 4.2 kg, supplier lead time is 3 days, and the supplier has the highest reliability-quality composite score under the current weight profile.

This is much stronger than showing a black-box prediction without justification.

---

## 6. Data strategy

The current data is useful for a demo but too small and static for serious evaluation. Use one of these approaches:

### Preferred approach: anonymized operational data

If you can obtain café transaction data, remove personal identifiers and document the anonymization process.

### Practical approach: synthetic data generator

Create a reproducible generator with:

- Weekly and yearly seasonality.
- Weekend effects.
- Random promotions.
- Supplier lead-time variability.
- Demand spikes.
- Spoilage and waste.
- Occasional stockouts.
- Price changes.

Store the seed and generator parameters. This allows the experiments to be reproduced.

### Minimum useful dataset

Aim for:

- At least 6–12 months of daily sales.
- At least 15–25 ingredients.
- Multiple suppliers per important ingredient.
- Purchase and delivery records.
- Inventory adjustments and waste.
- Enough events to test stockout and procurement behavior.

Include a formal data dictionary describing every field, unit, range and source.

---

## 7. Experimental design

Create an evaluation chapter, not only screenshots.

### Baselines

- Fixed reorder threshold.
- Moving-average forecast + fixed order quantity.
- Cheapest supplier selection.

### Proposed system

- Best-performing forecast model.
- Dynamic reorder point and safety stock.
- Multi-criteria or optimization-based supplier recommendation.

### Evaluation metrics

| Area | Metrics |
|---|---|
| Forecasting | MAE, RMSE, WAPE, bias |
| Inventory | Service level, fill rate, stockout days, average inventory, waste |
| Cost | Purchase cost, holding cost, shortage cost, total cost |
| Procurement | Lead-time adherence, supplier score, price variance |
| Software | API latency, test coverage, reliability, security findings |
| Usability | Task completion time, SUS questionnaire, user errors |

Use rolling-window evaluation and report confidence intervals or bootstrap intervals where appropriate. Include an ablation study showing the effect of removing each major component, such as promotions, safety stock or supplier reliability.

### Example hypotheses

- **H1:** Demand-aware reorder policies reduce stockout days compared with fixed thresholds.
- **H2:** Multi-criteria supplier selection reduces total procurement risk compared with cheapest-price selection.
- **H3:** The proposed system improves service level without increasing total inventory cost beyond an acceptable limit.
- **H4:** Explainable recommendations reduce decision time for procurement users.

---

## 8. Dashboard features that would make the project feel complete

Retain the visual identity of the current project, but replace static data with API-backed views.

### Manager dashboard

- Inventory health summary.
- Forecast accuracy by ingredient.
- Current stockout risk.
- Projected spend.
- Waste trend.
- Supplier risk heatmap.
- Recommended actions with explanations.

### Inventory page

- Search and filter.
- Stock history chart.
- Transaction ledger.
- Batch and expiry tracking.
- Manual adjustment with reason.
- Low-stock and expiring-soon alerts.

### Supplier page

- Supplier scorecard.
- Price history.
- Lead-time distribution, not only average lead time.
- Quality issue rate.
- Recommendation comparison and sensitivity analysis.

### Purchases page

- Purchase-order creation and approval.
- Partial receiving.
- Invoice/quantity variance.
- Delivery performance.

### Analytics page

- Forecast vs actual.
- What-if safety-stock simulator.
- Compare inventory policies.
- Exportable research tables and charts.

---

## 9. Engineering quality expected at master’s level

Add the following before presenting the project:

- Strong README with screenshots, architecture, setup, API examples and research contribution.
- Database migrations.
- `.env.example`; never commit secrets.
- Unit tests for domain calculations.
- API integration tests.
- End-to-end smoke tests for key user journeys.
- Type hints and static checking.
- Linting and formatting in CI.
- Docker Compose for the API and PostgreSQL.
- OpenAPI documentation.
- Structured logging and error handling.
- Input validation and safe authorization checks.
- Audit logging for stock and purchasing changes.
- Seed scripts and reproducible demo data.
- Backup and restore instructions.
- GitHub Actions for tests and quality checks.
- Versioned experiment configuration and results.

Target a meaningful test suite rather than a token coverage number. A reasonable initial target is 80%+ coverage for business logic, with critical inventory and procurement paths close to fully covered.

---

## 10. Suggested implementation sequence

### Phase 1 — Foundation

- Freeze the current UI as a baseline screenshot/demo.
- Create Python package structure.
- Define domain models and data dictionary.
- Add PostgreSQL/SQLite persistence and migrations.
- Import current `data.js` records into database seed data.

### Phase 2 — Backend conversion

- Build FastAPI routes for menu, inventory, suppliers and purchases.
- Replace browser data access with API calls.
- Implement inventory transaction ledger.
- Add authentication and roles.
- Add tests for stock status, stock deductions and purchase totals.

### Phase 3 — Operational workflows

- Add sales and recipe consumption.
- Add purchase-order lifecycle.
- Add receiving, waste and adjustments.
- Add audit log and notifications.

### Phase 4 — Research features

- Build reproducible synthetic data generator.
- Implement forecasting baselines and candidate models.
- Implement inventory policy simulation.
- Implement supplier ranking/optimization.
- Add evaluation reports and experiment tracking.

### Phase 5 — Product polish

- Connect dashboard charts to API endpoints.
- Add explainable recommendations.
- Improve accessibility and responsive behavior.
- Add Docker, CI and deployment documentation.
- Conduct user testing and usability evaluation.

### Phase 6 — Dissertation package

- Finalize research question and hypotheses.
- Document methodology and limitations.
- Run experiments using a fixed dataset and configuration.
- Report statistical and operational results.
- Include architecture, security and ethical considerations.
- Provide a reproducible repository and demo video.

---

## 11. What not to do

- Do not simply rename `.js` files to `.py`.
- Do not make a Python script that prints the same hard-coded tables.
- Do not add AI chat only for appearance; tie intelligence to forecasting or decisions.
- Do not use random train/test splitting for time-series data.
- Do not claim real-time behavior when data is static.
- Do not report model accuracy without comparing against a baseline.
- Do not hide assumptions about cost, shelf life, demand or supplier weights.
- Do not put all backend logic in one `main.py` file.
- Do not rely exclusively on notebooks; production logic belongs in tested modules.

---

## 12. Recommended minimum viable master’s scope

If time is limited, implement this focused version:

1. FastAPI + SQLAlchemy + PostgreSQL.
2. Users and two roles.
3. Ingredients, recipes, sales, inventory transactions and suppliers.
4. Moving-average and Holt-Winters forecasting.
5. Dynamic reorder point with safety stock.
6. TOPSIS or weighted supplier ranking.
7. Policy simulation against a fixed-threshold baseline.
8. Dashboard with forecast-vs-actual, stockout risk and recommendations.
9. Unit/API tests, Docker and CI.
10. A report with hypotheses, methodology, results, limitations and reproducibility instructions.

That scope is substantial enough to demonstrate software engineering, data engineering, machine learning, optimization and empirical evaluation without becoming unfinishable.

## 13. The strongest final demonstration

Show the same scenario under two systems:

- **Baseline:** fixed thresholds and cheapest supplier.
- **Brewline model:** forecast-aware inventory policy and multi-criteria supplier selection.

Then show:

- Fewer projected stockouts.
- The change in total procurement and holding cost.
- Supplier trade-offs.
- Forecast accuracy.
- The exact reasoning behind each recommended order.

That comparison will communicate the academic value much more effectively than adding more static pages.
