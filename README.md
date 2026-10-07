# Brewline Beans

**Brewline Beans** is a predictive café inventory and supplier optimization platform. It began as a static café management portal and now includes a Python/FastAPI backend, normalized persistence model, auditable inventory transactions, supplier recommendations, reorder analytics, automated tests and reproducible development tooling.

## Features

- FastAPI REST API with OpenAPI documentation.
- SQLAlchemy persistence with SQLite by default and PostgreSQL support through Docker.
- Ingredient, menu, recipe, supplier, purchase-order, forecast and inventory-transaction models.
- Auditable `RECEIPT`, `SALE`, `WASTE` and `ADJUSTMENT` stock movements.
- Dynamic stock health classification and reorder-point recommendations.
- Transparent supplier ranking based on price, lead time, quality and reliability.
- Role-based authentication with signed bearer tokens and audit events.
- Sales workflow that deducts recipe ingredients atomically from inventory.
- Baseline evaluation and fixed-threshold versus dynamic-policy simulation.
- Deterministic seed data for local demos.
- Pytest tests, Ruff linting, coverage reporting and GitHub Actions CI.
- Existing static UI retained as a visual prototype while the API becomes the source of truth.
- `live.html` provides an API-backed operations view for live inventory and reorder analysis.
- `operations.html` provides API-backed batch, expiry and notification views.
- All original pages now load their menu, inventory, supplier and purchase data through `data.js`, which reads the REST API and falls back to `data.static.js` only when the API is unavailable.
- Budget-constrained supplier allocation is available at `POST /api/analytics/allocate`.
- Batch and alert workflows are available under `/api/operations`.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m scripts.seed
uvicorn app.main:app --reload
```

Open:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

The seeded demo manager is `manager` with password `BrewlineDemo123!`. Change or remove this account before any deployment.

## Example API calls

```bash
curl http://localhost:8000/api/inventory
curl http://localhost:8000/api/suppliers/1/recommendations
curl 'http://localhost:8000/api/analytics/reorder/1?daily_demand=2&lead_time_days=3'
curl -X POST 'http://localhost:8000/api/analytics/simulate?initial_stock=10&reorder_point=5&order_quantity=10' -H 'Content-Type: application/json' -d '[8,10,2,12,4,9]'
curl -X POST 'http://localhost:8000/api/inventory/1/transactions' \\
  -H 'Content-Type: application/json' \\
  -d '{"quantity": 2, "transaction_type": "WASTE", "reason": "Daily spoilage"}'
```

## Docker

```bash
docker compose up --build
```

The Docker stack starts PostgreSQL and the API. The default local development mode uses SQLite so that the project can be run without infrastructure.

## Test and quality checks

```bash
pytest --cov=app --cov-report=term-missing
ruff check app tests scripts
```

## Project structure

- `app/main.py`: FastAPI application and routes.
- `app/db/models.py`: normalized SQLAlchemy domain model.
- `app/services/`: business rules such as inventory adjustments.
- `app/analytics/`: forecasting, reorder and supplier-ranking logic.
- `scripts/seed.py`: reproducible demonstration data.
- `tests/`: domain and API tests.
- `docs/`: architecture and data dictionary.
- `MASTERS_PROJECT_ROADMAP.md`: full implementation and dissertation roadmap.

## Research roadmap

The next research iteration should add daily sales data, time-series cross-validation, Holt-Winters/SARIMA/gradient-boosting comparisons, inventory-policy simulation, supplier-allocation constraints, confidence intervals and a usability study. The baseline should remain fixed-threshold replenishment plus cheapest-supplier selection.

Generate the reproducible experiment report with:

```bash
python -m scripts.generate_experiment_report
```

The resulting methodology, metrics, results and limitations are documented in `docs/experiment-report.md`.

## License

This project is provided for academic and educational use. Add an institutional or open-source license before distributing it publicly.
