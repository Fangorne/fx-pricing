"""Unit tests for YahooFinanceProvider — yfinance is fully patched, no network."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.infrastructure.providers.yahoo_finance import YahooFinanceProvider, _fetch_sync


def _make_fast_info(bid: float = 0.0, ask: float = 0.0, last_price: float = 0.0) -> MagicMock:
    info = MagicMock()
    info.bid = bid
    info.ask = ask
    info.last_price = last_price
    return info


def _patch_ticker(fast_info: MagicMock):
    ticker = MagicMock()
    ticker.fast_info = fast_info
    return patch("app.infrastructure.providers.yahoo_finance.yfinance.Ticker", return_value=ticker)


# --- _fetch_sync unit tests (synchronous, no event loop needed) ---


def test_fetch_sync_bid_ask_present():
    info = _make_fast_info(bid=1.0800, ask=1.0810, last_price=1.0805)
    with _patch_ticker(info):
        spot = _fetch_sync("EUR/USD", "EURUSD=X", timeout=5)
    assert spot.bid == pytest.approx(1.0800)
    assert spot.ask == pytest.approx(1.0810)
    assert spot.pair == "EUR/USD"
    assert spot.timestamp.tzinfo is not None


def test_fetch_sync_fallback_to_last_price():
    info = _make_fast_info(bid=0.0, ask=0.0, last_price=150.25)
    with _patch_ticker(info):
        spot = _fetch_sync("USD/JPY", "USDJPY=X", timeout=5)
    assert spot.bid == pytest.approx(150.25)
    assert spot.ask == pytest.approx(150.25)


def test_fetch_sync_no_price_raises():
    info = _make_fast_info(bid=0.0, ask=0.0, last_price=0.0)
    with _patch_ticker(info), pytest.raises(MarketDataUnavailableError, match="USD/JPY"):
        _fetch_sync("USD/JPY", "USDJPY=X", timeout=5)


def test_fetch_sync_yfinance_exception_raises():
    with patch("app.infrastructure.providers.yahoo_finance.yfinance.Ticker", side_effect=RuntimeError("network error")):
        with pytest.raises(MarketDataUnavailableError, match="network error"):
            _fetch_sync("EUR/USD", "EURUSD=X", timeout=5)


# --- YahooFinanceProvider async tests ---


@pytest.mark.asyncio
async def test_get_spot_known_pair():
    info = _make_fast_info(bid=1.2700, ask=1.2705)
    with _patch_ticker(info):
        provider = YahooFinanceProvider()
        spot = await provider.get_spot("GBP/USD")
    assert isinstance(spot, SpotPrice)
    assert spot.pair == "GBP/USD"


@pytest.mark.asyncio
async def test_get_spot_unknown_pair_raises():
    provider = YahooFinanceProvider()
    with pytest.raises(MarketDataUnavailableError, match="XXX/YYY"):
        await provider.get_spot("XXX/YYY")


@pytest.mark.asyncio
async def test_get_spots_returns_successful_only():
    call_count = 0

    def make_ticker(symbol: str) -> MagicMock:
        nonlocal call_count
        call_count += 1
        ticker = MagicMock()
        if symbol == "EURUSD=X":
            ticker.fast_info = _make_fast_info(bid=1.08, ask=1.081)
        else:
            # Simulate missing data for GBP/USD
            ticker.fast_info = _make_fast_info(bid=0.0, ask=0.0, last_price=0.0)
        return ticker

    with patch("app.infrastructure.providers.yahoo_finance.yfinance.Ticker", side_effect=make_ticker):
        provider = YahooFinanceProvider()
        result = await provider.get_spots(["EUR/USD", "GBP/USD"])

    assert "EUR/USD" in result
    assert "GBP/USD" not in result  # failed silently


@pytest.mark.asyncio
async def test_get_spots_all_succeed():
    info = _make_fast_info(bid=1.08, ask=1.081)
    with _patch_ticker(info):
        provider = YahooFinanceProvider()
        result = await provider.get_spots(["EUR/USD", "GBP/USD", "USD/JPY"])
    assert len(result) == 3


@pytest.mark.asyncio
async def test_get_spots_empty_list():
    provider = YahooFinanceProvider()
    result = await provider.get_spots([])
    assert result == {}
