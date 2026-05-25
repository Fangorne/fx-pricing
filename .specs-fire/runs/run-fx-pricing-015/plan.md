# Plan — run-fx-pricing-015 / db-sqlalchemy-models

## Work Item: SQLAlchemy Models (conventions, calendriers, holidays)

### Approach
Créer la couche infrastructure DB : moteur async SQLAlchemy 2.0, session factory, dependency FastAPI `get_db()`, et les trois modèles ORM mappant le domaine FX existant.

### Files to Create
- `backend/app/infrastructure/database.py` — AsyncEngine, AsyncSessionLocal, get_db()
- `backend/app/infrastructure/models.py` — Base, FxConventionModel, MarketCalendarModel, HolidayModel

### Files to Modify
- `backend/app/infrastructure/__init__.py` — exports

### Tests
- `backend/tests/unit/test_models.py` — 6 tests sur les métadonnées et l'instanciation des modèles

### Schema DB
```
fx_conventions (pair PK VARCHAR(7), spot_lag INT, day_count VARCHAR(20),
                roll_convention VARCHAR(30), pip_precision INT, quotation_side VARCHAR(10))
market_calendars (currency PK VARCHAR(3), name VARCHAR(50))
holidays (id PK SERIAL, currency FK VARCHAR(3), holiday_date DATE, description VARCHAR(100))
```
