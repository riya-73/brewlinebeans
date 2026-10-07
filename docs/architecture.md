# Architecture

## Overview

Brewline uses a layered architecture:

```text
Browser / existing static UI
          |
       REST API (FastAPI)
          |
   Services and analytics
          |
 SQLAlchemy domain model
          |
 SQLite (local) / PostgreSQL (Docker)
```

## Domain boundaries

- **Menu:** sellable menu items and normalized recipes.
- **Inventory:** ingredients and immutable stock movements.
- **Procurement:** suppliers and purchase-order lifecycle.
- **Analytics:** forecast baselines, reorder policy and supplier ranking.

## Inventory invariants

1. A `SALE` or `WASTE` transaction cannot reduce stock below zero.
2. A purchase receipt increases stock and creates a `RECEIPT` transaction.
3. A purchase order cannot receive more than its outstanding quantity.
4. Every manual stock adjustment requires a reason.
5. Current stock is the operational balance; the transaction ledger is the audit trail.

## Analytics decisions

The initial forecasting implementation deliberately uses a moving-average baseline. A baseline is necessary before introducing more complex models. The reorder policy exposes its assumptions so that the dissertation can compare service factor, lead time and forecast quality.

Supplier ranking is transparent rather than opaque: price and lead time are cost criteria; quality and reliability are benefit criteria. The weights are configurable in the analytics service for sensitivity analysis.

## Production hardening still required

- Alembic migrations rather than `create_all` for deployed schema changes.
- Authentication and role-based authorization.
- Rate limiting and structured audit events for all sensitive endpoints.
- PostgreSQL-specific integration tests.
- Background jobs for scheduled forecast generation.
- Frontend migration from `data.js` to API-backed data fetching.
