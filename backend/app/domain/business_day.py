"""Business day adjustment conventions for FX date generation."""

from __future__ import annotations

import calendar as _cal
import enum
from datetime import date, timedelta

from app.domain.calendar import MarketCalendar


class BusinessDayConvention(enum.Enum):
    """Standard ISDA business day adjustment conventions."""

    FOLLOWING = "FOLLOWING"
    MODIFIED_FOLLOWING = "MODIFIED_FOLLOWING"
    PRECEDING = "PRECEDING"
    MODIFIED_PRECEDING = "MODIFIED_PRECEDING"
    END_OF_MONTH = "END_OF_MONTH"


def _next_bd(d: date, cal: MarketCalendar) -> date:
    candidate = d + timedelta(days=1)
    while not cal.is_business_day(candidate):
        candidate += timedelta(days=1)
    return candidate


def _prev_bd(d: date, cal: MarketCalendar) -> date:
    candidate = d - timedelta(days=1)
    while not cal.is_business_day(candidate):
        candidate -= timedelta(days=1)
    return candidate


def _last_bd_of_month(d: date, cal: MarketCalendar) -> date:
    """Return the last business day of d's month."""
    last_day = _cal.monthrange(d.year, d.month)[1]
    candidate = date(d.year, d.month, last_day)
    while not cal.is_business_day(candidate):
        candidate -= timedelta(days=1)
    return candidate


def _first_bd_of_month(d: date, cal: MarketCalendar) -> date:
    """Return the first business day of d's month."""
    candidate = date(d.year, d.month, 1)
    while not cal.is_business_day(candidate):
        candidate += timedelta(days=1)
    return candidate


def adjust(d: date, convention: BusinessDayConvention, cal: MarketCalendar) -> date:
    """Adjust d to a business day according to convention.

    If d is already a business day, all conventions except END_OF_MONTH
    return d unchanged.
    """
    if convention is BusinessDayConvention.END_OF_MONTH:
        return _last_bd_of_month(d, cal)

    if cal.is_business_day(d):
        return d

    if convention is BusinessDayConvention.FOLLOWING:
        return _next_bd(d, cal)

    if convention is BusinessDayConvention.MODIFIED_FOLLOWING:
        nxt = _next_bd(d, cal)
        if nxt.month != d.month:
            return _last_bd_of_month(d, cal)
        return nxt

    if convention is BusinessDayConvention.PRECEDING:
        return _prev_bd(d, cal)

    if convention is BusinessDayConvention.MODIFIED_PRECEDING:
        prv = _prev_bd(d, cal)
        if prv.month != d.month:
            return _first_bd_of_month(d, cal)
        return prv

    raise ValueError(f"Unknown convention: {convention}")  # pragma: no cover
