"""FastAPI dependency providers for market data infrastructure."""

from __future__ import annotations

from typing import Annotated

import redis.asyncio as aioredis
from fastapi import Depends

from app.config import get_settings
from app.infrastructure.cache.price_cache import PriceCache
from app.infrastructure.providers.base import MarketDataProvider
from app.infrastructure.providers.yahoo_finance import YahooFinanceProvider


def get_redis() -> aioredis.Redis:
    settings = get_settings()
    return aioredis.from_url(settings.effective_redis_url, decode_responses=True)


def get_provider() -> MarketDataProvider:
    return YahooFinanceProvider(timeout=get_settings().market_data_cache_ttl_seconds)


def get_price_cache(redis: Annotated[aioredis.Redis, Depends(get_redis)]) -> PriceCache:
    settings = get_settings()
    return PriceCache(
        redis=redis,
        ttl=settings.market_data_cache_ttl_seconds,
        stale_threshold=settings.market_data_stale_threshold_seconds,
    )
