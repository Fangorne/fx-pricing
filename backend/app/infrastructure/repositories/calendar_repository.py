"""Repository for market calendar and holiday reference data."""

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.calendar import MarketCalendar
from app.infrastructure.models import HolidayModel, MarketCalendarModel


class _DbBackedCalendar(MarketCalendar):
    """A MarketCalendar whose holidays come from pre-fetched DB rows."""

    def __init__(self, name: str, holidays_by_year: dict[int, frozenset[date]]) -> None:
        super().__init__(name=name, rules=[])
        self._db_data = holidays_by_year

    def holidays(self, year: int) -> frozenset[date]:
        if year not in self._cache:
            self._cache[year] = self._db_data.get(year, frozenset())
        return self._cache[year]


class CalendarRepository:
    """Repository for market calendars and holiday data."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_currency(self, currency: str) -> MarketCalendar | None:
        """Return a MarketCalendar backed by DB holidays, or None if unknown."""
        result = await self._session.execute(
            select(MarketCalendarModel).where(
                MarketCalendarModel.currency == currency.upper()
            )
        )
        cal_row = result.scalar_one_or_none()
        if cal_row is None:
            return None

        # Load all stored holidays for this currency
        h_result = await self._session.execute(
            select(HolidayModel)
            .where(HolidayModel.currency == currency.upper())
            .order_by(HolidayModel.holiday_date)
        )
        holidays_by_year: dict[int, set[date]] = {}
        for h in h_result.scalars():
            holidays_by_year.setdefault(h.holiday_date.year, set()).add(h.holiday_date)

        return _DbBackedCalendar(
            name=cal_row.name,
            holidays_by_year={y: frozenset(s) for y, s in holidays_by_year.items()},
        )

    async def get_holidays(self, currency: str, year: int) -> frozenset[date]:
        """Return the stored holidays for a currency and year."""
        result = await self._session.execute(
            select(HolidayModel.holiday_date).where(
                HolidayModel.currency == currency.upper(),
                HolidayModel.holiday_date >= date(year, 1, 1),
                HolidayModel.holiday_date <= date(year, 12, 31),
            )
        )
        return frozenset(result.scalars())
