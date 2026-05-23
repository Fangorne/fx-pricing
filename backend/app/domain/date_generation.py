"""FX spot and value date generation."""

from __future__ import annotations

import calendar as _cal
from datetime import date, timedelta

from app.domain.business_day import BusinessDayConvention, adjust
from app.domain.calendar import MarketCalendar
from app.domain.types import CurrencyPair, Tenor

# ---------------------------------------------------------------------------
# Spot lag registry — T+2 default, T+1 exceptions
# ---------------------------------------------------------------------------

# Keys are canonical pair strings (base/quote as traded in the market).
# USD/CAD is traded as USDCAD with USD as base → T+1.
# All others default to T+2 unless listed here.
SPOT_LAGS: dict[str, int] = {
    "USD/CAD": 1,
    "CAD/USD": 1,
    "USD/TRY": 1,
    "TRY/USD": 1,
    "USD/RUB": 1,
    "RUB/USD": 1,
}

_DEFAULT_SPOT_LAG = 2


def _spot_lag(pair: CurrencyPair) -> int:
    return SPOT_LAGS.get(str(pair), _DEFAULT_SPOT_LAG)


# ---------------------------------------------------------------------------
# Month arithmetic — handles month-end overflow (Jan 31 + 1M → Feb 28/29)
# ---------------------------------------------------------------------------

def _add_months(d: date, months: int) -> date:
    """Add an integer number of months to d, clamping to month-end on overflow."""
    total_months = d.month - 1 + months
    year = d.year + total_months // 12
    month = total_months % 12 + 1
    last_day = _cal.monthrange(year, month)[1]
    day = min(d.day, last_day)
    return date(year, month, day)


# ---------------------------------------------------------------------------
# EOM detection
# ---------------------------------------------------------------------------

def _is_last_bd_of_month(d: date, cal: MarketCalendar) -> bool:
    """Return True if d is the last business day of its month."""
    last_day = _cal.monthrange(d.year, d.month)[1]
    candidate = date(d.year, d.month, last_day)
    while not cal.is_business_day(candidate):
        candidate -= timedelta(days=1)
    return d == candidate


# ---------------------------------------------------------------------------
# spot_date
# ---------------------------------------------------------------------------

def spot_date(
    trade_date: date,
    pair: CurrencyPair,
    cal: MarketCalendar,
) -> date:
    """Return the spot settlement date for a G10 FX pair.

    Adds spot_lag business days from trade_date using cal, then applies
    MODIFIED_FOLLOWING to land on a valid business day.
    """
    lag = _spot_lag(pair)
    candidate = trade_date
    remaining = lag
    while remaining > 0:
        candidate += timedelta(days=1)
        if cal.is_business_day(candidate):
            remaining -= 1
    return adjust(candidate, BusinessDayConvention.MODIFIED_FOLLOWING, cal)


# ---------------------------------------------------------------------------
# value_date
# ---------------------------------------------------------------------------

def value_date(
    trade_date: date,
    tenor: Tenor,
    pair: CurrencyPair,
    cal: MarketCalendar,
    convention: BusinessDayConvention = BusinessDayConvention.MODIFIED_FOLLOWING,
) -> date:
    """Return the value (settlement) date for an FX trade.

    Special tenors (ON, TN, SN) are handled before the spot date is computed.
    All other tenors start from spot and add the tenor period.
    EOM rule: if spot_date is the last BD of its month, the result is pinned
    to the last BD of the target month.
    """
    label = tenor.label

    # --- Short-end tenors (pre-spot) ---

    if label == "ON":
        # Overnight: trade_date + 1 BD
        return _next_bd(trade_date, cal)

    if label == "TN":
        # Tom-next: trade_date + 1 BD (same as ON for T+2 pairs; spot - 1 BD)
        return _next_bd(trade_date, cal)

    # Compute spot for all other tenors
    sd = spot_date(trade_date, pair, cal)

    if label == "SN":
        # Spot-next: spot + 1 BD
        return _next_bd(sd, cal)

    # --- Week tenors ---

    if label.endswith("W"):
        weeks = int(label[:-1])
        candidate = sd + timedelta(weeks=weeks)
        return adjust(candidate, convention, cal)

    # --- Month and year tenors ---

    if label.endswith("M"):
        months = int(label[:-1])
        eom = _is_last_bd_of_month(sd, cal)
        candidate = _add_months(sd, months)
        if eom:
            return adjust(candidate, BusinessDayConvention.END_OF_MONTH, cal)
        return adjust(candidate, convention, cal)

    if label.endswith("Y"):
        years = int(label[:-1])
        eom = _is_last_bd_of_month(sd, cal)
        candidate = _add_months(sd, years * 12)
        if eom:
            return adjust(candidate, BusinessDayConvention.END_OF_MONTH, cal)
        return adjust(candidate, convention, cal)

    raise ValueError(f"Unrecognised tenor label: {label!r}")  # pragma: no cover


# ---------------------------------------------------------------------------
# Private helper
# ---------------------------------------------------------------------------

def _next_bd(d: date, cal: MarketCalendar) -> date:
    candidate = d + timedelta(days=1)
    while not cal.is_business_day(candidate):
        candidate += timedelta(days=1)
    return candidate
