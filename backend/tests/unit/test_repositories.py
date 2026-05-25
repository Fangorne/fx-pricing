"""Unit tests for repository layer — mocked AsyncSession, no live DB."""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.business_day import BusinessDayConvention
from app.domain.conventions import DayCountBasis, FXConvention
from app.domain.types import QuotationSide
from app.infrastructure.models import FxConventionModel, HolidayModel, MarketCalendarModel
from app.infrastructure.repositories.calendar_repository import CalendarRepository
from app.infrastructure.repositories.convention_repository import ConventionRepository


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_session() -> AsyncMock:
    """Return a minimal AsyncSession mock."""
    session = AsyncMock()
    return session


def _scalars_result(rows: list) -> MagicMock:
    result = MagicMock()
    result.scalars.return_value = rows
    return result


def _scalar_one_or_none_result(row) -> MagicMock:
    result = MagicMock()
    result.scalar_one_or_none.return_value = row
    return result


def _eur_usd_model() -> MagicMock:
    m = MagicMock(spec=FxConventionModel)
    m.pair = "EUR/USD"
    m.spot_lag = 2
    m.day_count = "Act/360"
    m.roll_convention = "MODIFIED_FOLLOWING"
    m.pip_precision = 4
    m.quotation_side = "direct"
    return m


def _usd_calendar_model() -> MagicMock:
    m = MagicMock(spec=MarketCalendarModel)
    m.currency = "USD"
    m.name = "USD/FED"
    return m


# ---------------------------------------------------------------------------
# ConventionRepository
# ---------------------------------------------------------------------------


class TestConventionRepository:
    async def test_get_all_returns_mapped_conventions(self) -> None:
        session = _make_session()
        session.execute.return_value = _scalars_result([_eur_usd_model()])

        repo = ConventionRepository(session)
        results = await repo.get_all()

        assert len(results) == 1
        pair, conv = results[0]
        assert pair == "EUR/USD"
        assert isinstance(conv, FXConvention)
        assert conv.spot_lag == 2
        assert conv.day_count is DayCountBasis.ACT_360
        assert conv.roll_convention is BusinessDayConvention.MODIFIED_FOLLOWING
        assert conv.pip_precision == 4
        assert conv.quotation_side is QuotationSide.DIRECT

    async def test_get_by_pair_found(self) -> None:
        session = _make_session()
        session.execute.return_value = _scalar_one_or_none_result(_eur_usd_model())

        repo = ConventionRepository(session)
        conv = await repo.get_by_pair("EUR/USD")

        assert conv is not None
        assert conv.spot_lag == 2

    async def test_get_by_pair_not_found_returns_none(self) -> None:
        session = _make_session()
        session.execute.return_value = _scalar_one_or_none_result(None)

        repo = ConventionRepository(session)
        result = await repo.get_by_pair("XXX/YYY")

        assert result is None

    async def test_get_all_empty(self) -> None:
        session = _make_session()
        session.execute.return_value = _scalars_result([])

        repo = ConventionRepository(session)
        results = await repo.get_all()

        assert results == []


# ---------------------------------------------------------------------------
# CalendarRepository
# ---------------------------------------------------------------------------


class TestCalendarRepository:
    async def test_get_by_currency_returns_market_calendar(self) -> None:
        session = _make_session()
        cal_result = _scalar_one_or_none_result(_usd_calendar_model())
        holiday_row = MagicMock(spec=HolidayModel)
        holiday_row.holiday_date = date(2026, 1, 1)
        holiday_row.currency = "USD"
        h_result = _scalars_result([holiday_row])
        session.execute.side_effect = [cal_result, h_result]

        repo = CalendarRepository(session)
        cal = await repo.get_by_currency("USD")

        assert cal is not None
        assert cal.name == "USD/FED"
        assert date(2026, 1, 1) in cal.holidays(2026)

    async def test_get_by_currency_unknown_returns_none(self) -> None:
        session = _make_session()
        session.execute.return_value = _scalar_one_or_none_result(None)

        repo = CalendarRepository(session)
        result = await repo.get_by_currency("XYZ")

        assert result is None

    async def test_get_holidays_returns_frozenset(self) -> None:
        session = _make_session()
        result = MagicMock()
        result.scalars.return_value = [date(2026, 1, 1), date(2026, 12, 25)]
        session.execute.return_value = result

        repo = CalendarRepository(session)
        holidays = await repo.get_holidays("USD", 2026)

        assert isinstance(holidays, frozenset)
        assert date(2026, 1, 1) in holidays
        assert date(2026, 12, 25) in holidays

    async def test_get_holidays_empty_year(self) -> None:
        session = _make_session()
        result = MagicMock()
        result.scalars.return_value = []
        session.execute.return_value = result

        repo = CalendarRepository(session)
        holidays = await repo.get_holidays("USD", 1900)

        assert holidays == frozenset()

    async def test_db_backed_calendar_missing_year_returns_empty(self) -> None:
        session = _make_session()
        cal_result = _scalar_one_or_none_result(_usd_calendar_model())
        h_result = _scalars_result([])
        session.execute.side_effect = [cal_result, h_result]

        repo = CalendarRepository(session)
        cal = await repo.get_by_currency("USD")

        assert cal is not None
        assert cal.holidays(2099) == frozenset()
