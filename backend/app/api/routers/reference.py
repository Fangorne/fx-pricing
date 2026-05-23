"""Reference data router — FX conventions, calendars, and date calculations."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.reference import (
    BusinessDayResponse,
    ConventionResponse,
    HolidayResponse,
    SpotDateResponse,
    ValueDateResponse,
)
from app.domain.calendar import CombinedCalendar, get_calendar
from app.domain.conventions import FX_CONVENTIONS, get_convention
from app.domain.date_generation import spot_date, value_date
from app.domain.exceptions import UnsupportedCurrencyPairError
from app.domain.types import CurrencyPair, Tenor

router = APIRouter(prefix="/api/v1", tags=["reference"])


def _parse_pair(pair: str) -> CurrencyPair:
    try:
        return CurrencyPair.from_string(pair)
    except (ValueError, KeyError):
        raise HTTPException(status_code=422, detail=f"Invalid currency pair: {pair!r}")


def _build_calendar(cp: CurrencyPair) -> CombinedCalendar:
    try:
        base_cal = get_calendar(str(cp.base))
        quote_cal = get_calendar(str(cp.quote))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return CombinedCalendar(base_cal, quote_cal)


# ---------------------------------------------------------------------------
# Conventions
# ---------------------------------------------------------------------------


@router.get("/conventions", response_model=list[ConventionResponse])
async def list_conventions() -> list[ConventionResponse]:
    """List all registered FX conventions."""
    return [
        ConventionResponse(
            pair=pair,
            spot_lag=conv.spot_lag,
            day_count=str(conv.day_count),
            roll_convention=conv.roll_convention.value,
            pip_precision=conv.pip_precision,
            quotation_side=conv.quotation_side.value,
        )
        for pair, conv in FX_CONVENTIONS.items()
    ]


# {pair:path} captures slashes so "EUR/USD" works as well as "EURUSD"
@router.get("/conventions/{pair:path}", response_model=ConventionResponse)
async def get_convention_detail(pair: str) -> ConventionResponse:
    """Return the FX convention for a specific pair (e.g. EURUSD or EUR/USD)."""
    try:
        conv = get_convention(pair)
    except UnsupportedCurrencyPairError:
        raise HTTPException(status_code=404, detail=f"No convention for pair {pair!r}")
    canonical = pair.strip().upper()
    if "/" not in canonical and len(canonical) == 6:  # noqa: PLR2004
        canonical = f"{canonical[:3]}/{canonical[3:]}"
    return ConventionResponse(
        pair=canonical,
        spot_lag=conv.spot_lag,
        day_count=str(conv.day_count),
        roll_convention=conv.roll_convention.value,
        pip_precision=conv.pip_precision,
        quotation_side=conv.quotation_side.value,
    )


# ---------------------------------------------------------------------------
# Calendars
# ---------------------------------------------------------------------------


@router.get("/calendars/{currency}/holidays", response_model=list[HolidayResponse])
async def get_holidays(
    currency: str,
    year: int = Query(..., ge=2000, le=2100),
) -> list[HolidayResponse]:
    """Return all holidays for a currency in a given year."""
    try:
        cal = get_calendar(currency)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"No calendar for currency {currency!r}")
    holidays = sorted(cal.holidays(year))
    return [HolidayResponse(date=h, name=f"{currency} holiday") for h in holidays]


@router.get("/calendars/{currency}/business-day", response_model=BusinessDayResponse)
async def check_business_day(
    currency: str,
    date: Annotated[date, Query(...)],  # type: ignore[valid-type]
) -> BusinessDayResponse:
    """Check whether a date is a business day for a given currency."""
    try:
        cal = get_calendar(currency)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"No calendar for currency {currency!r}")
    is_bd = cal.is_business_day(date)
    reason: str | None = None
    if not is_bd:
        if date.weekday() >= 5:  # noqa: PLR2004
            reason = "Weekend"
        else:
            reason = "Public holiday"
    return BusinessDayResponse(
        date=date,
        currency=currency.upper(),
        is_business_day=is_bd,
        reason=reason,
    )


# ---------------------------------------------------------------------------
# Date calculations
# ---------------------------------------------------------------------------


@router.get("/spot-dates/{pair}", response_model=SpotDateResponse)
async def calculate_spot_date(
    pair: str,
    trade_date: Annotated[date, Query(...)],  # type: ignore[valid-type]
) -> SpotDateResponse:
    """Return the spot settlement date for a currency pair."""
    cp = _parse_pair(pair)
    try:
        get_convention(cp)
    except UnsupportedCurrencyPairError:
        raise HTTPException(status_code=404, detail=f"No convention for pair {pair!r}")
    cal = _build_calendar(cp)
    sd = spot_date(trade_date, cp, cal)
    return SpotDateResponse(pair=str(cp), trade_date=trade_date, spot_date=sd)


@router.get("/spot-dates/{pair}/value", response_model=ValueDateResponse)
async def calculate_value_date(
    pair: str,
    trade_date: Annotated[date, Query(...)],  # type: ignore[valid-type]
    tenor: str = Query(...),
) -> ValueDateResponse:
    """Return the value date for a currency pair and tenor."""
    cp = _parse_pair(pair)
    try:
        conv = get_convention(cp)
    except UnsupportedCurrencyPairError:
        raise HTTPException(status_code=404, detail=f"No convention for pair {pair!r}")
    cal = _build_calendar(cp)
    try:
        t = Tenor.from_string(tenor)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    sd = spot_date(trade_date, cp, cal)
    vd = value_date(trade_date, t, cp, cal, conv.roll_convention)
    return ValueDateResponse(
        pair=str(cp),
        trade_date=trade_date,
        tenor=t.label,
        spot_date=sd,
        value_date=vd,
    )
