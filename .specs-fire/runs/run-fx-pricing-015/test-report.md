# Test Report — run-fx-pricing-015 / db-sqlalchemy-models

## Test Results
- Passed: 6
- Failed: 0
- Skipped: 0

## Suite: `tests/unit/test_models.py`

| Test | Status |
|------|--------|
| test_fx_convention_model_table | ✅ |
| test_market_calendar_model_table | ✅ |
| test_holiday_model_table | ✅ |
| test_all_models_registered_in_base | ✅ |
| test_fx_convention_instantiation | ✅ |
| test_holiday_instantiation | ✅ |

## Acceptance Criteria Validation

- [x] `app/infrastructure/database.py` contient le moteur async et `AsyncSession`
- [x] `app/infrastructure/models.py` définit `FxConventionModel`, `MarketCalendarModel`, `HolidayModel`
- [x] Les modèles utilisent `DeclarativeBase` SQLAlchemy 2.0 (style moderne)
- [x] Les types de colonnes correspondent au domaine FX
- [x] `get_db()` dependency injectable dans FastAPI
