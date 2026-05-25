# Walkthrough — run-fx-pricing-016 / db-alembic-migrations

## What Was Built

Alembic async migration setup + initial migration + idempotent seed script for G10 FX reference data.

## Files Created

### `backend/alembic.ini`
Standard Alembic config with `script_location = alembic`. The `sqlalchemy.url` default is overridden at runtime by `env.py` reading from `Settings.effective_database_url`.

### `backend/alembic/env.py`
Async env using `create_async_engine` + `connection.run_sync()` for both online and offline modes. Imports `Base` from `app.infrastructure.models` so autogenerate picks up all three models. Handles `postgresql://` → `postgresql+asyncpg://` coercion.

### `backend/alembic/versions/0001_initial_fx_tables.py`
Hand-written initial migration — no live DB required. Creates:
- `fx_conventions` (pair PK, spot_lag, day_count, roll_convention, pip_precision, quotation_side)
- `market_calendars` (currency PK, name)
- `holidays` (id SERIAL PK, currency FK→market_calendars CASCADE, holiday_date, description, index on currency)

Full `downgrade()` drops tables in reverse dependency order.

### `backend/scripts/seed.py`
Async seed using `INSERT ... ON CONFLICT DO NOTHING` — safe to run multiple times. Inserts:
- 10 market calendars (USD/FED, EUR/ECB, GBP/BOE, JPY/BOJ, CHF/SNB, CAD/BOC, AUD/RBA, NZD/RBNZ, SEK/RIX, NOK/NB)
- 12 FX conventions sourced directly from `app.domain.conventions.FX_CONVENTIONS`

Run with: `python -m scripts.seed` from `backend/`

## Usage

```bash
# Apply migration
cd backend
alembic upgrade head

# Seed reference data
python -m scripts.seed

# Rollback
alembic downgrade base
```

## Next Work Item

`db-repository-layer` — async CRUD repository wrapping these models.
