"""Redis-backed price cache for FX spot prices."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from redis.asyncio import Redis

from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.infrastructure.providers.base import MarketDataProvider

logger = logging.getLogger(__name__)

_KEY_PREFIX = "fx:spot:"


def _key(pair: str) -> str:
    return f"{_KEY_PREFIX}{pair}"


def _encode(price: SpotPrice) -> str:
    return json.dumps(
        {
            "pair": price.pair,
            "bid": price.bid,
            "ask": price.ask,
            "timestamp": price.timestamp.isoformat(),
        }
    )


def _decode(pair: str, raw: str) -> SpotPrice:
    data = json.loads(raw)
    return SpotPrice(
        pair=data["pair"],
        bid=data["bid"],
        ask=data["ask"],
        timestamp=datetime.fromisoformat(data["timestamp"]).replace(tzinfo=timezone.utc),
    )


class PriceCache:
    """Cache-aside wrapper around Redis for FX spot prices.

    Args:
        redis: Async Redis client (injected — no singleton).
        ttl: Seconds before a cached entry expires (hard TTL in Redis).
        stale_threshold: Seconds after which a price is considered stale for
            the domain. Used for graceful degradation: if the provider fails
            but a stale entry exists, the stale price is returned rather than
            raising.
    """

    def __init__(self, redis: Redis, ttl: int = 30, stale_threshold: int = 60) -> None:
        self._redis = redis
        self._ttl = ttl
        self._stale_threshold = stale_threshold

    async def get(self, pair: str) -> SpotPrice | None:
        """Return cached price or None if absent."""
        raw = await self._redis.get(_key(pair))
        if raw is None:
            return None
        return _decode(pair, raw)

    async def set(self, pair: str, price: SpotPrice) -> None:
        """Store price in Redis with the configured TTL."""
        await self._redis.setex(_key(pair), self._ttl, _encode(price))

    async def get_or_fetch(self, pair: str, provider: MarketDataProvider) -> SpotPrice:
        """Return cached price if available, otherwise fetch from provider.

        Graceful degradation: if the provider fails and a stale cached value
        exists (beyond TTL but still in Redis), return it rather than raising.
        The Redis TTL is intentionally set longer than the domain stale
        threshold to enable this fallback window.
        """
        cached = await self.get(pair)
        if cached is not None and not cached.is_stale(self._stale_threshold):
            return cached

        try:
            fresh = await provider.get_spot(pair)
            await self.set(pair, fresh)
            return fresh
        except MarketDataUnavailableError:
            if cached is not None:
                logger.warning("Provider failed for %s — returning stale cached price", pair)
                return cached
            raise
