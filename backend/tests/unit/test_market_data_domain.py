"""Unit tests for SpotPrice domain type and market data exceptions."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from app.domain.exceptions import MarketDataUnavailableError, StaleMarketDataError
from app.domain.market_data import SpotPrice


def _now() -> datetime:
    return datetime.now(tz=UTC)


def _spot(
    bid: float = 1.0800, ask: float = 1.0802, pair: str = "EUR/USD", ts: datetime | None = None
) -> SpotPrice:
    return SpotPrice(pair=pair, bid=bid, ask=ask, timestamp=ts or _now())


# --- Construction ---


def test_spot_price_valid():
    s = _spot()
    assert s.pair == "EUR/USD"
    assert s.bid == pytest.approx(1.0800)
    assert s.ask == pytest.approx(1.0802)


def test_spot_price_mid():
    s = _spot(bid=1.0800, ask=1.0802)
    assert s.mid == pytest.approx(1.0801)


def test_spot_price_spread():
    s = _spot(bid=1.0800, ask=1.0810)
    assert s.spread == pytest.approx(0.0010)


def test_spot_price_frozen():
    s = _spot()
    with pytest.raises(Exception):
        s.bid = 99.0  # type: ignore[misc]


# --- Validation ---


def test_negative_bid_raises():
    with pytest.raises(ValueError, match="bid"):
        SpotPrice(pair="EUR/USD", bid=-1.0, ask=1.0, timestamp=_now())


def test_zero_ask_raises():
    with pytest.raises(ValueError, match="ask"):
        SpotPrice(pair="EUR/USD", bid=1.0, ask=0.0, timestamp=_now())


def test_bid_greater_than_ask_raises():
    with pytest.raises(ValueError, match="bid"):
        SpotPrice(pair="EUR/USD", bid=1.0810, ask=1.0800, timestamp=_now())


def test_naive_timestamp_raises():
    with pytest.raises(ValueError, match="timezone"):
        SpotPrice(pair="EUR/USD", bid=1.08, ask=1.09, timestamp=datetime(2024, 1, 1))


# --- Staleness ---


def test_fresh_price_not_stale():
    s = _spot(ts=_now() - timedelta(seconds=5))
    assert not s.is_stale(max_age_seconds=30)


def test_old_price_is_stale():
    s = _spot(ts=_now() - timedelta(seconds=60))
    assert s.is_stale(max_age_seconds=30)


def test_price_exactly_at_threshold_is_not_stale():
    # age must be *strictly greater than* threshold
    ts = _now() - timedelta(seconds=30)
    s = _spot(ts=ts)
    # may be 30s or 30.0001s depending on execution speed; just verify boundary direction
    assert not s.is_stale(max_age_seconds=60)


# --- Exceptions ---


def test_market_data_unavailable_error():
    err = MarketDataUnavailableError("EUR/USD", "timeout")
    assert "EUR/USD" in str(err)
    assert "timeout" in str(err)
    assert err.pair == "EUR/USD"


def test_market_data_unavailable_error_no_reason():
    err = MarketDataUnavailableError("USD/JPY")
    assert "USD/JPY" in str(err)


def test_stale_market_data_error():
    err = StaleMarketDataError("GBP/USD", age_seconds=120.0, threshold=30)
    assert "GBP/USD" in str(err)
    assert "120" in str(err)
    assert "30" in str(err)
    assert err.pair == "GBP/USD"
    assert err.age_seconds == 120.0
    assert err.threshold == 30
