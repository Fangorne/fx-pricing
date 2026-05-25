"""Seed script — inserts G10 FX conventions and market calendars.

Idempotent: uses INSERT ... ON CONFLICT DO NOTHING.
Run from backend/: python -m scripts.seed
"""

import asyncio

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from app.domain.conventions import FX_CONVENTIONS
from app.infrastructure.database import AsyncSessionLocal, engine
from app.infrastructure.models import Base, FxConventionModel, MarketCalendarModel

CALENDAR_NAMES: dict[str, str] = {
    "USD": "USD/FED",
    "EUR": "EUR/ECB",
    "GBP": "GBP/BOE",
    "JPY": "JPY/BOJ",
    "CHF": "CHF/SNB",
    "CAD": "CAD/BOC",
    "AUD": "AUD/RBA",
    "NZD": "NZD/RBNZ",
    "SEK": "SEK/RIX",
    "NOK": "NOK/NB",
}


async def seed() -> None:
    # Ensure tables exist (safe if already created by Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # --- Market calendars ---
        for currency, name in CALENDAR_NAMES.items():
            stmt = (
                insert(MarketCalendarModel)
                .values(currency=currency, name=name)
                .on_conflict_do_nothing(index_elements=["currency"])
            )
            await session.execute(stmt)

        # --- FX conventions ---
        for pair_str, conv in FX_CONVENTIONS.items():
            stmt = (
                insert(FxConventionModel)
                .values(
                    pair=pair_str,
                    spot_lag=conv.spot_lag,
                    day_count=conv.day_count.value,
                    roll_convention=conv.roll_convention.value,
                    pip_precision=conv.pip_precision,
                    quotation_side=conv.quotation_side.value,
                )
                .on_conflict_do_nothing(index_elements=["pair"])
            )
            await session.execute(stmt)

        await session.commit()

    # Row counts
    async with AsyncSessionLocal() as session:
        cal_count = (await session.execute(text("SELECT COUNT(*) FROM market_calendars"))).scalar()
        conv_count = (await session.execute(text("SELECT COUNT(*) FROM fx_conventions"))).scalar()

    print(f"Seed complete — {cal_count} calendars, {conv_count} conventions")


if __name__ == "__main__":
    asyncio.run(seed())
