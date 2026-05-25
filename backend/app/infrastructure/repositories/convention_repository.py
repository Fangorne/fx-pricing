"""Repository for FX convention reference data."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.business_day import BusinessDayConvention
from app.domain.conventions import DayCountBasis, FXConvention
from app.domain.types import QuotationSide
from app.infrastructure.models import FxConventionModel


def _to_convention(row: FxConventionModel) -> FXConvention:
    return FXConvention(
        spot_lag=row.spot_lag,
        day_count=DayCountBasis(row.day_count),
        roll_convention=BusinessDayConvention(row.roll_convention),
        pip_precision=row.pip_precision,
        quotation_side=QuotationSide(row.quotation_side),
    )


class ConventionRepository:
    """Read-only repository for FX conventions stored in PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> list[tuple[str, FXConvention]]:
        """Return all conventions as (pair_str, FXConvention) tuples."""
        result = await self._session.execute(
            select(FxConventionModel).order_by(FxConventionModel.pair)
        )
        return [(row.pair, _to_convention(row)) for row in result.scalars()]

    async def get_by_pair(self, pair: str) -> FXConvention | None:
        """Return the convention for a specific pair, or None if not found."""
        result = await self._session.execute(
            select(FxConventionModel).where(FxConventionModel.pair == pair.upper())
        )
        row = result.scalar_one_or_none()
        return _to_convention(row) if row is not None else None
