"""Unit tests for SQLAlchemy ORM models."""

from datetime import date

from sqlalchemy import inspect

from app.infrastructure.models import Base, FxConventionModel, HolidayModel, MarketCalendarModel


def test_fx_convention_model_table():
    mapper = inspect(FxConventionModel)
    cols = {c.key for c in mapper.mapper.column_attrs}
    assert "pair" in cols
    assert "spot_lag" in cols
    assert "day_count" in cols
    assert "roll_convention" in cols
    assert "pip_precision" in cols
    assert "quotation_side" in cols
    assert FxConventionModel.__tablename__ == "fx_conventions"


def test_market_calendar_model_table():
    mapper = inspect(MarketCalendarModel)
    cols = {c.key for c in mapper.mapper.column_attrs}
    assert "currency" in cols
    assert "name" in cols
    assert MarketCalendarModel.__tablename__ == "market_calendars"


def test_holiday_model_table():
    mapper = inspect(HolidayModel)
    cols = {c.key for c in mapper.mapper.column_attrs}
    assert "id" in cols
    assert "currency" in cols
    assert "holiday_date" in cols
    assert "description" in cols
    assert HolidayModel.__tablename__ == "holidays"


def test_all_models_registered_in_base():
    tables = set(Base.metadata.tables.keys())
    assert "fx_conventions" in tables
    assert "market_calendars" in tables
    assert "holidays" in tables


def test_fx_convention_instantiation():
    conv = FxConventionModel(
        pair="EUR/USD",
        spot_lag=2,
        day_count="Act/360",
        roll_convention="MODIFIED_FOLLOWING",
        pip_precision=4,
        quotation_side="direct",
    )
    assert conv.pair == "EUR/USD"
    assert conv.spot_lag == 2


def test_holiday_instantiation():
    h = HolidayModel(
        currency="USD",
        holiday_date=date(2026, 1, 1),
        description="New Year's Day",
    )
    assert h.currency == "USD"
    assert h.holiday_date == date(2026, 1, 1)
