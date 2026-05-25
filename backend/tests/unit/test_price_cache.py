"""Unit tests for PriceCache — uses fakeredis, no real Redis."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest
import fakeredis.aioredis

from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.infrastructure.cache.price_cache import PriceCache


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _spot(pair: str = "EUR/USD", bid: float = 1.08, ask: float = 1.081, age_seconds: float = 0) -> SpotPrice:
    ts = _now() - timedelta(seconds=age_seconds)
    return SpotPrice(pair=pair, bid=bid, ask=ask, timestamp=ts)


@pytest.fixture
async def redis():
    r = fakeredis.aioredis.FakeRedis()
    yield r
    await r.aclose()


@pytest.fixture
def cache(redis):
    return PriceCache(redis=redis, ttl=30, stale_threshold=60)


# --- get / set ---


@pytest.mark.asyncio
async def test_get_returns_none_when_empty(cache):
    result = await cache.get("EUR/USD")
    assert result is None


@pytest.mark.asyncio
async def test_set_and_get_roundtrip(cache):
    price = _spot()
    await cache.set("EUR/USD", price)
    result = await cache.get("EUR/USD")
    assert result is not None
    assert result.pair == "EUR/USD"
    assert result.bid == pytest.approx(1.08)
    assert result.ask == pytest.approx(1.081)
    assert result.timestamp.tzinfo is not None


@pytest.mark.asyncio
async def test_get_different_pair_returns_none(cache):
    await cache.set("EUR/USD", _spot("EUR/USD"))
    result = await cache.get("GBP/USD")
    assert result is None


# --- get_or_fetch: cache hit ---


@pytest.mark.asyncio
async def test_get_or_fetch_returns_cached_when_fresh(cache):
    fresh = _spot(age_seconds=5)
    await cache.set("EUR/USD", fresh)

    provider = AsyncMock()
    result = await cache.get_or_fetch("EUR/USD", provider)

    provider.get_spot.assert_not_called()
    assert result.bid == pytest.approx(1.08)


# --- get_or_fetch: cache miss ---


@pytest.mark.asyncio
async def test_get_or_fetch_calls_provider_on_miss(cache):
    fetched = _spot(age_seconds=0)
    provider = AsyncMock()
    provider.get_spot.return_value = fetched

    result = await cache.get_or_fetch("EUR/USD", provider)

    provider.get_spot.assert_called_once_with("EUR/USD")
    assert result.bid == pytest.approx(1.08)


@pytest.mark.asyncio
async def test_get_or_fetch_stores_result_after_fetch(cache):
    fetched = _spot()
    provider = AsyncMock()
    provider.get_spot.return_value = fetched

    await cache.get_or_fetch("EUR/USD", provider)

    # Second call should hit cache, not provider
    await cache.get_or_fetch("EUR/USD", provider)
    provider.get_spot.assert_called_once()


# --- get_or_fetch: stale cache + provider failure (graceful degradation) ---


@pytest.mark.asyncio
async def test_get_or_fetch_returns_stale_when_provider_fails(cache):
    stale = _spot(age_seconds=90)  # older than stale_threshold=60
    await cache.set("EUR/USD", stale)

    provider = AsyncMock()
    provider.get_spot.side_effect = MarketDataUnavailableError("EUR/USD", "timeout")

    result = await cache.get_or_fetch("EUR/USD", provider)
    assert result.bid == pytest.approx(1.08)  # stale value returned


@pytest.mark.asyncio
async def test_get_or_fetch_raises_when_provider_fails_and_no_cache(cache):
    provider = AsyncMock()
    provider.get_spot.side_effect = MarketDataUnavailableError("EUR/USD", "timeout")

    with pytest.raises(MarketDataUnavailableError):
        await cache.get_or_fetch("EUR/USD", provider)


# --- stale detection triggers re-fetch ---


@pytest.mark.asyncio
async def test_get_or_fetch_refetches_stale_price(cache):
    stale = _spot(age_seconds=90)
    await cache.set("EUR/USD", stale)

    fresh = _spot(age_seconds=0, bid=1.09, ask=1.091)
    provider = AsyncMock()
    provider.get_spot.return_value = fresh

    result = await cache.get_or_fetch("EUR/USD", provider)
    provider.get_spot.assert_called_once()
    assert result.bid == pytest.approx(1.09)
