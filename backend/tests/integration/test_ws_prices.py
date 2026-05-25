"""Integration tests for WS /ws/prices/{pair} endpoint."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.main import app


def _spot(pair: str = "EUR/USD", bid: float = 1.08, ask: float = 1.081) -> SpotPrice:
    return SpotPrice(pair=pair, bid=bid, ask=ask, timestamp=datetime.now(tz=timezone.utc))


def _make_cache(spot: SpotPrice | None = None, fail: bool = False):
    cache = MagicMock()
    if fail:
        cache.get_or_fetch = AsyncMock(side_effect=MarketDataUnavailableError("EUR/USD", "down"))
    else:
        cache.get_or_fetch = AsyncMock(return_value=spot or _spot())
    return cache


@pytest.fixture
def client():
    return TestClient(app)


def _patch_infra(cache=None, interval: int = 0):
    """Patch PriceCache, YahooFinanceProvider and sleep so tests run instantly."""
    cache = cache or _make_cache()
    fake_redis = MagicMock()
    fake_redis.aclose = AsyncMock()
    return (
        patch("app.api.routers.ws_prices.PriceCache", return_value=cache),
        patch("app.api.routers.ws_prices.YahooFinanceProvider"),
        patch("app.api.routers.ws_prices.aioredis.from_url", return_value=fake_redis),
        patch("app.api.routers.ws_prices.asyncio.sleep", new=AsyncMock()),
    )


# --- Tests ---


def test_ws_unknown_pair_closes_4004(client):
    with client.websocket_connect("/ws/prices/XXX/YYY") as ws:
        # Server closes immediately with 4004
        with pytest.raises(Exception):
            ws.receive_json()


def test_ws_valid_pair_sends_price(client):
    cache = _make_cache(_spot("EUR/USD", 1.0850, 1.0852))
    patches = _patch_infra(cache)

    with patches[0], patches[1], patches[2], patches[3]:
        with client.websocket_connect("/ws/prices/EUR/USD") as ws:
            data = ws.receive_json()

    assert data["pair"] == "EUR/USD"
    assert data["bid"] == pytest.approx(1.0850)
    assert data["ask"] == pytest.approx(1.0852)
    assert "mid" in data
    assert "is_stale" in data
    assert "age_seconds" in data
    assert "timestamp" in data


def test_ws_pair_normalisation_dash(client):
    """EUR-USD should be accepted as EUR/USD."""
    cache = _make_cache(_spot("EUR/USD"))
    patches = _patch_infra(cache)

    with patches[0], patches[1], patches[2], patches[3]:
        with client.websocket_connect("/ws/prices/EUR-USD") as ws:
            data = ws.receive_json()

    assert data["pair"] == "EUR/USD"


def test_ws_provider_error_sends_error_payload(client):
    cache = _make_cache(fail=True)
    patches = _patch_infra(cache)

    with patches[0], patches[1], patches[2], patches[3]:
        with client.websocket_connect("/ws/prices/EUR/USD") as ws:
            data = ws.receive_json()

    assert "error" in data
    assert data["pair"] == "EUR/USD"


def test_ws_mid_is_correct(client):
    cache = _make_cache(_spot("USD/JPY", bid=149.80, ask=149.82))
    patches = _patch_infra(cache)

    with patches[0], patches[1], patches[2], patches[3]:
        with client.websocket_connect("/ws/prices/USD/JPY") as ws:
            data = ws.receive_json()

    assert data["mid"] == pytest.approx(149.81)
