from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.domain.calendar import get_calendar
from app.domain.conventions import FX_CONVENTIONS
from app.infrastructure.database import get_db
from app.infrastructure.models import Base, FxConventionModel, HolidayModel, MarketCalendarModel
from app.main import app

_CALENDAR_NAMES: dict[str, str] = {
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

_SEED_YEARS = range(2024, 2028)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed conventions
    async with session_factory() as session:
        for pair_str, conv in FX_CONVENTIONS.items():
            session.add(FxConventionModel(
                pair=pair_str,
                spot_lag=conv.spot_lag,
                day_count=conv.day_count.value,
                roll_convention=conv.roll_convention.value,
                pip_precision=conv.pip_precision,
                quotation_side=conv.quotation_side.value,
            ))

        # Seed calendars + holidays
        for currency, name in _CALENDAR_NAMES.items():
            session.add(MarketCalendarModel(currency=currency, name=name))
            cal = get_calendar(currency)
            for year in _SEED_YEARS:
                for h_date in sorted(cal.holidays(year)):
                    session.add(HolidayModel(
                        currency=currency,
                        holiday_date=h_date,
                        description=f"{currency} holiday",
                    ))

        await session.commit()

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            yield c
    finally:
        app.dependency_overrides.pop(get_db, None)
        await engine.dispose()
