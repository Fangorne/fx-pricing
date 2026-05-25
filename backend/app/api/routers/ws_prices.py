"""WebSocket router — streaming live FX spot prices."""

from __future__ import annotations

import asyncio
from datetime import datetime

import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pytz import UTC

from app.config import get_settings
from app.domain.conventions import FX_CONVENTIONS
from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.infrastructure.cache.price_cache import PriceCache
from app.infrastructure.providers.yahoo_finance import YahooFinanceProvider

router = APIRouter()


def _price_payload(price: SpotPrice, stale_threshold: int) -> dict:
    now = datetime.now(tz=UTC)
    age = (now - price.timestamp).total_seconds()
    return {
        "pair": price.pair,
        "bid": price.bid,
        "ask": price.ask,
        "mid": price.mid,
        "timestamp": price.timestamp.isoformat(),
        "is_stale": price.is_stale(stale_threshold),
        "age_seconds": round(age, 1),
    }


@router.websocket("/ws/prices/{pair:path}")
async def ws_spot_price(websocket: WebSocket, pair: str) -> None:
    """Stream live spot price for a currency pair.

    Pushes a JSON payload every `ws_price_interval_seconds` seconds.
    Closes with code 4004 if the pair is unknown.
    On provider error, sends `{"error": "...", "pair": "..."}` and continues.
    """
    settings = get_settings()
    pair = pair.upper().replace("-", "/")

    await websocket.accept()

    if pair not in FX_CONVENTIONS:
        await websocket.close(code=4004, reason=f"Unsupported pair: {pair!r}")
        return

    redis_client = aioredis.from_url(settings.effective_redis_url, decode_responses=True)
    # TTL matches the push interval so each tick fetches a fresh price.
    # The REST cache (30s) stays independent — this only affects the WS loop.
    cache = PriceCache(
        redis=redis_client,
        ttl=settings.ws_price_interval_seconds,
        stale_threshold=settings.market_data_stale_threshold_seconds,
    )
    provider = YahooFinanceProvider(timeout=settings.market_data_cache_ttl_seconds)

    try:
        while True:
            try:
                price = await cache.get_or_fetch(pair, provider)
                await websocket.send_json(
                    _price_payload(price, settings.market_data_stale_threshold_seconds)
                )
            except MarketDataUnavailableError as exc:
                await websocket.send_json({"error": str(exc), "pair": pair})
            await asyncio.sleep(settings.ws_price_interval_seconds)
    except WebSocketDisconnect:
        pass
    finally:
        await redis_client.aclose()
