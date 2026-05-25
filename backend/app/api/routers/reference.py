"""Reference data router — FX conventions, calendars, and date calculations."""

from __future__ import annotations

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.reference import (
    BusinessDayResponse,
    ConventionResponse,
    HolidayResponse,
    SpotDateResponse,
    ValueDateResponse,
)
from app.domain.date_generation import spot_date, value_date
from app.domain.exceptions import UnsupportedCurrencyPairError
from app.domain.types import CurrencyPair, Tenor
from app.infrastructure.database import get_db
from app.infrastructure.repositories import CalendarRepository, ConventionRepository

router = APIRouter(prefix="/api/v1", tags=["reference"])


def _parse_pair(pair: str) -> CurrencyPair:
    try:
        return CurrencyPair.from_string(pair)
    except (ValueError, KeyError):
        raise HTTPException(status_code=422, detail=f"Invalid currency pair: {pair!r}")


# ---------------------------------------------------------------------------
# Conventions
# ---------------------------------------------------------------------------


@router.get("/conventions", response_model=list[ConventionResponse])
async def list_conventions(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ConventionResponse]:
    """List all registered FX conventions."""
    repo = ConventionRepository(db)
    rows = await repo.get_all()
    return [
        ConventionResponse(
            pair=pair,
            spot_lag=conv.spot_lag,
            day_count=str(conv.day_count),
            roll_convention=conv.roll_convention.value,
            pip_precision=conv.pip_precision,
            quotation_side=conv.quotation_side.value,
        )
        for pair, conv in rows
    ]


@router.get("/conventions/{pair:path}", response_model=ConventionResponse)
async def get_convention_detail(
    pair: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ConventionResponse:
    """Return the FX convention for a specific pair (e.g. EURUSD or EUR/USD)."""
    canonical = pair.strip().upper()
    if "/" not in canonical and len(canonical) == 6:  # noqa: PLR2004
        canonical = f"{canonical[:3]}/{canonical[3:]}"

    repo = ConventionRepository(db)
    conv = await repo.get_by_pair(canonical)
    if conv is None:
        raise HTTPException(status_code=404, detail=f"No convention for pair {pair!r}")

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
    db: AsyncSession = Depends(get_db),
) -> list[HolidayResponse]:
    """Return all holidays for a currency in a given year."""
    repo = CalendarRepository(db)
    cal = await repo.get_by_currency(currency)
    if cal is None:
        raise HTTPException(status_code=404, detail=f"No calendar for currency {currency!r}")
    holidays = sorted(await repo.get_holidays(currency, year))
    return [HolidayResponse(date=h, name=f"{currency.upper()} holiday") for h in holidays]


@router.get("/calendars/{currency}/business-day", response_model=BusinessDayResponse)
async def check_business_day(
    currency: str,
    date: Annotated[date, Query(...)],  # type: ignore[valid-type]
    db: AsyncSession = Depends(get_db),
) -> BusinessDayResponse:
    """Check whether a date is a business day for a given currency."""
    repo = CalendarRepository(db)
    cal = await repo.get_by_currency(currency)
    if cal is None:
        raise HTTPException(status_code=404, detail=f"No calendar for currency {currency!r}")
    is_bd = cal.is_business_day(date)
    reason: str | None = None
    if not is_bd:
        reason = "Weekend" if date.weekday() >= 5 else "Public holiday"  # noqa: PLR2004
    return BusinessDayResponse(
        date=date,
        currency=currency.upper(),
        is_business_day=is_bd,
        reason=reason,
    )


# ---------------------------------------------------------------------------
# Date calculations
# ---------------------------------------------------------------------------


@router.get("/spot-dates", response_model=SpotDateResponse)
async def calculate_spot_date(
    pair: str = Query(...),
    trade_date: Annotated[date, Query(...)] = ...,  # type: ignore[valid-type]
    db: AsyncSession = Depends(get_db),
) -> SpotDateResponse:
    """Return the spot settlement date for a currency pair."""
    cp = _parse_pair(pair)
    conv_repo = ConventionRepository(db)
    cal_repo = CalendarRepository(db)

    conv = await conv_repo.get_by_pair(str(cp))
    if conv is None:
        raise HTTPException(status_code=404, detail=f"No convention for pair {pair!r}")

    base_cal = await cal_repo.get_by_currency(str(cp.base))
    quote_cal = await cal_repo.get_by_currency(str(cp.quote))
    if base_cal is None or quote_cal is None:
        raise HTTPException(status_code=404, detail=f"Calendar not found for pair {pair!r}")

    from app.domain.calendar import CombinedCalendar
    cal = CombinedCalendar(base_cal, quote_cal)
    sd = spot_date(trade_date, cp, cal)
    return SpotDateResponse(pair=str(cp), trade_date=trade_date, spot_date=sd)


@router.get("/spot-dates/value", response_model=ValueDateResponse)
async def calculate_value_date(
    pair: str = Query(...),
    trade_date: Annotated[date, Query(...)] = ...,  # type: ignore[valid-type]
    tenor: str = Query(...),
    db: AsyncSession = Depends(get_db),
) -> ValueDateResponse:
    """Return the value date for a currency pair and tenor."""
    cp = _parse_pair(pair)
    conv_repo = ConventionRepository(db)
    cal_repo = CalendarRepository(db)

    conv = await conv_repo.get_by_pair(str(cp))
    if conv is None:
        raise HTTPException(status_code=404, detail=f"No convention for pair {pair!r}")

    base_cal = await cal_repo.get_by_currency(str(cp.base))
    quote_cal = await cal_repo.get_by_currency(str(cp.quote))
    if base_cal is None or quote_cal is None:
        raise HTTPException(status_code=404, detail=f"Calendar not found for pair {pair!r}")

    try:
        t = Tenor.from_string(tenor)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    from app.domain.calendar import CombinedCalendar
    cal = CombinedCalendar(base_cal, quote_cal)
    sd = spot_date(trade_date, cp, cal)
    vd = value_date(trade_date, t, cp, cal, conv.roll_convention)
    return ValueDateResponse(
        pair=str(cp),
        trade_date=trade_date,
        tenor=t.label,
        spot_date=sd,
        value_date=vd,
    )
