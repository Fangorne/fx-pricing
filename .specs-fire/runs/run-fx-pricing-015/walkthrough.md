# Walkthrough — run-fx-pricing-015 / db-sqlalchemy-models

## What Was Built

Infrastructure layer for async database access using SQLAlchemy 2.0, with three ORM models mapping the existing FX domain types.

## Files Created

### `backend/app/infrastructure/database.py`
Async engine + session factory using `sqlalchemy.ext.asyncio`. Reads `DATABASE_URL` from `app.config.get_settings().effective_database_url`. Exposes `get_db()` as a FastAPI-injectable async generator yielding `AsyncSession` per request.

### `backend/app/infrastructure/models.py`
Three ORM models using SQLAlchemy 2.0 `DeclarativeBase` + `Mapped`/`mapped_column` style:

- **`FxConventionModel`** (`fx_conventions`) — `pair` PK VARCHAR(7), `spot_lag` INT, `day_count` VARCHAR(20), `roll_convention` VARCHAR(30), `pip_precision` INT, `quotation_side` VARCHAR(10)
- **`MarketCalendarModel`** (`market_calendars`) — `currency` PK VARCHAR(3), `name` VARCHAR(50), relationship → holidays
- **`HolidayModel`** (`holidays`) — `id` SERIAL PK, `currency` FK→market_calendars, `holiday_date` DATE, `description` VARCHAR(100), index on currency

## Files Modified

### `backend/app/infrastructure/__init__.py`
Added exports for all public symbols: `engine`, `AsyncSessionLocal`, `get_db`, `Base`, `FxConventionModel`, `MarketCalendarModel`, `HolidayModel`.

## Tests

`backend/tests/unit/test_models.py` — 6 tests, all passing:
- Column metadata inspection for each model
- All three tables registered in `Base.metadata`
- Instantiation smoke tests for `FxConventionModel` and `HolidayModel`

## Next Work Item

`db-alembic-migrations` — initial Alembic migration from these models.
