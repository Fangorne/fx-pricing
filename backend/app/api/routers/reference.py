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

router = APIRouter(prefix="/api/v1")

_404 = {404: {"description": "Resource not found"}}
_422 = {422: {"description": "Invalid input (bad pair format, out-of-range date, etc.)"}}


def _parse_pair(pair: str) -> CurrencyPair:
    try:
        return CurrencyPair.from_string(pair)
    except (ValueError, KeyError):
        raise HTTPException(status_code=422, detail=f"Invalid currency pair: {pair!r}")


# ---------------------------------------------------------------------------
# Conventions
# ---------------------------------------------------------------------------


@router.get(
    "/conventions",
    tags=["Conventions"],
    response_model=list[ConventionResponse],
    summary="List all FX conventions",
    description=(
        "Returns market conventions for all registered G10 currency pairs: "
        "spot lag (in business days), day count basis, roll convention, "
        "pip precision, and quotation side."
    ),
    response_description="Ordered list of FX conventions",
)
async def list_conventions(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ConventionResponse]:
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


@router.get(
    "/conventions/{pair:path}",
    tags=["Conventions"],
    response_model=ConventionResponse,
    summary="Get convention for a specific pair",
    description=(
        "Returns the market convention for a single currency pair. "
        "Accepts both slash format (`EUR/USD`) and no-slash format (`EURUSD`)."
    ),
    response_description="FX convention for the requested pair",
    responses={**_404, **_422},
)
async def get_convention_detail(
    pair: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ConventionResponse:
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


@router.get(
    "/calendars/{currency}/holidays",
    tags=["Calendars"],
    response_model=list[HolidayResponse],
    summary="List holidays for a currency",
    description=(
        "Returns all public holidays for the given G10 currency in the requested year. "
        "Holidays follow official central bank schedules "
        "(FED for USD, ECB for EUR, BOE for GBP, etc.)."
    ),
    response_description="Sorted list of holiday dates",
    responses=_404,
)
async def get_holidays(
    currency: str,
    year: int = Query(..., ge=2000, le=2100, description="Calendar year", examples=[2026]),
    db: AsyncSession = Depends(get_db),
) -> list[HolidayResponse]:
    repo = CalendarRepository(db)
    cal = await repo.get_by_currency(currency)
    if cal is None:
        raise HTTPException(status_code=404, detail=f"No calendar for currency {currency!r}")
    holidays = sorted(await repo.get_holidays(currency, year))
    return [HolidayResponse(date=h, name=f"{currency.upper()} holiday") for h in holidays]


@router.get(
    "/calendars/{currency}/business-day",
    tags=["Calendars"],
    response_model=BusinessDayResponse,
    summary="Check if a date is a business day",
    description=(
        "Returns whether the given date is a business day for the specified currency. "
        "Weekends and public holidays are excluded. "
        "The `reason` field is set when the date is not a business day."
    ),
    response_description="Business day status with optional reason",
    responses=_404,
)
async def check_business_day(
    currency: str,
    date: Annotated[date, Query(..., description="Date to check (YYYY-MM-DD)", examples=["2026-05-26"])],  # type: ignore[valid-type]
    db: AsyncSession = Depends(get_db),
) -> BusinessDayResponse:
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


@router.get(
    "/spot-dates",
    tags=["Date Calculator"],
    response_model=SpotDateResponse,
    summary="Calculate spot settlement date",
    description=(
        "Returns the spot settlement date for a currency pair given a trade date. "
        "Applies the pair's spot lag and business day adjustment rules "
        "using the combined calendar of both currencies."
    ),
    response_description="Spot date result",
    responses={**_404, **_422},
)
async def calculate_spot_date(
    pair: str = Query(..., description="Currency pair (e.g. EUR/USD or EURUSD)", examples=["EUR/USD"]),
    trade_date: Annotated[date, Query(..., description="Trade date (YYYY-MM-DD)", examples=["2026-05-22"])] = ...,  # type: ignore[valid-type]
    db: AsyncSession = Depends(get_db),
) -> SpotDateResponse:
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


@router.get(
    "/spot-dates/value",
    tags=["Date Calculator"],
    response_model=ValueDateResponse,
    summary="Calculate value date for a tenor",
    description=(
        "Returns both the spot date and the forward value date for a currency pair, "
        "trade date, and tenor (e.g. 3M, 1Y). "
        "Applies Modified Following roll convention by default, "
        "adjusted for the combined currency calendar."
    ),
    response_description="Value date result including spot date",
    responses={**_404, **_422},
)
async def calculate_value_date(
    pair: str = Query(..., description="Currency pair (e.g. EUR/USD)", examples=["EUR/USD"]),
    trade_date: Annotated[date, Query(..., description="Trade date (YYYY-MM-DD)", examples=["2026-05-22"])] = ...,  # type: ignore[valid-type]
    tenor: str = Query(..., description="Tenor label (ON, TN, 1W, 1M, 3M, 6M, 1Y…)", examples=["3M"]),
    db: AsyncSession = Depends(get_db),
) -> ValueDateResponse:
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
