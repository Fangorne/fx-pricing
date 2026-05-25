"""Integration tests for /api/v1/prices endpoints.

Provider and Redis are fully mocked via FastAPI dependency overrides.
No real network or Redis connections are made.
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_price_cache, get_provider
from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.infrastructure.cache.price_cache import PriceCache
from app.main import app


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _spot(pair: str = "EUR/USD", bid: float = 1.08, ask: float = 1.081) -> SpotPrice:
    return SpotPrice(pair=pair, bid=bid, ask=ask, timestamp=_now())


def _make_cache(spot: SpotPrice | None = None, fail: bool = False) -> PriceCache:
    cache = MagicMock(spec=PriceCache)
    cache._stale_threshold = 60
    if fail:
        cache.get_or_fetch = AsyncMock(side_effect=MarketDataUnavailableError("EUR/USD", "down"))
    else:
        cache.get_or_fetch = AsyncMock(return_value=spot or _spot())
    return cache


def _make_provider() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def client_with(request):
    """Factory fixture: call client_with(cache, provider) to build a TestClient."""
    def _build(cache=None, provider=None):
        cache = cache or _make_cache()
        provider = provider or _make_provider()
        app.dependency_overrides[get_price_cache] = lambda: cache
        app.dependency_overrides[get_provider] = lambda: provider
        c = TestClient(app, raise_server_exceptions=False)
        return c
    yield _build
    app.dependency_overrides.clear()


# --- Single pair ---


def test_get_spot_price_ok(client_with):
    client = client_with(cache=_make_cache(_spot("EUR/USD", 1.0850, 1.0852)))
    resp = client.get("/api/v1/prices/EUR/USD")
    assert resp.status_code == 200
    data = resp.json()
    assert data["pair"] == "EUR/USD"
    assert data["bid"] == pytest.approx(1.0850)
    assert data["ask"] == pytest.approx(1.0852)
    assert "mid" in data
    assert "is_stale" in data
    assert "age_seconds" in data


def test_get_spot_price_unknown_pair_404(client_with):
    client = client_with()
    resp = client.get("/api/v1/prices/XXX/YYY")
    assert resp.status_code == 404


def test_get_spot_price_provider_down_no_cache_503(client_with):
    client = client_with(cache=_make_cache(fail=True))
    resp = client.get("/api/v1/prices/EUR/USD")
    assert resp.status_code == 503


def test_get_spot_price_slash_encoding(client_with):
    """EUR-USD (dash) should be normalised to EUR/USD."""
    client = client_with(cache=_make_cache(_spot("EUR/USD")))
    resp = client.get("/api/v1/prices/EUR-USD")
    assert resp.status_code == 200


def test_get_spot_price_mid_is_correct(client_with):
    client = client_with(cache=_make_cache(_spot("EUR/USD", bid=1.08, ask=1.082)))
    resp = client.get("/api/v1/prices/EUR/USD")
    assert resp.json()["mid"] == pytest.approx(1.081)


# --- Multiple pairs ---


def test_get_spot_prices_all(client_with):
    cache = MagicMock(spec=PriceCache)
    cache._stale_threshold = 60
    cache.get_or_fetch = AsyncMock(side_effect=lambda pair, _p: _spot(pair))
    client = client_with(cache=cache)
    resp = client.get("/api/v1/prices")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) > 0


def test_get_spot_prices_filtered(client_with):
    cache = MagicMock(spec=PriceCache)
    cache._stale_threshold = 60
    cache.get_or_fetch = AsyncMock(side_effect=lambda pair, _p: _spot(pair))
    client = client_with(cache=cache)
    resp = client.get("/api/v1/prices?pairs=EUR/USD,USD/JPY")
    assert resp.status_code == 200
    pairs = [r["pair"] for r in resp.json()]
    assert "EUR/USD" in pairs
    assert "USD/JPY" in pairs
    assert len(pairs) == 2


def test_get_spot_prices_unknown_pair_in_filter_404(client_with):
    client = client_with()
    resp = client.get("/api/v1/prices?pairs=EUR/USD,XXX/YYY")
    assert resp.status_code == 404


def test_get_spot_prices_failed_pair_omitted(client_with):
    """Pairs that fail individually are silently omitted in bulk fetch."""
    async def _side_effect(pair, _p):
        if pair == "EUR/USD":
            return _spot("EUR/USD")
        raise MarketDataUnavailableError(pair, "down")

    cache = MagicMock(spec=PriceCache)
    cache._stale_threshold = 60
    cache.get_or_fetch = AsyncMock(side_effect=_side_effect)
    client = client_with(cache=cache)
    resp = client.get("/api/v1/prices?pairs=EUR/USD,GBP/USD")
    assert resp.status_code == 200
    pairs = [r["pair"] for r in resp.json()]
    assert pairs == ["EUR/USD"]
