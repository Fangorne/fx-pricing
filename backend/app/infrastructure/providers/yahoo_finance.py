"""Yahoo Finance market data provider adapter."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

import yfinance

from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.infrastructure.providers.base import MarketDataProvider

# Maps standard FX pair notation to Yahoo Finance ticker symbols.
# Yahoo convention: EURUSD=X means "price of EUR in USD".
_PAIR_TO_TICKER: dict[str, str] = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "USD/CHF": "USDCHF=X",
    "USD/CAD": "USDCAD=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "EUR/GBP": "EURGBP=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "EUR/CHF": "EURCHF=X",
    "EUR/CAD": "EURCAD=X",
    "EUR/AUD": "EURAUD=X",
    "EUR/NZD": "EURNZD=X",
    "GBP/CHF": "GBPCHF=X",
    "AUD/JPY": "AUDJPY=X",
    "AUD/NZD": "AUDNZD=X",
    "USD/SEK": "USDSEK=X",
    "USD/NOK": "USDNOK=X",
}


def _fetch_sync(pair: str, ticker_symbol: str, timeout: int) -> SpotPrice:
    """Blocking fetch — intended to run in a thread pool."""
    try:
        ticker: Any = yfinance.Ticker(ticker_symbol)
        info = ticker.fast_info
        bid: float = getattr(info, "bid", 0.0) or 0.0
        ask: float = getattr(info, "ask", 0.0) or 0.0
        last: float = getattr(info, "last_price", 0.0) or 0.0

        # Fall back to last_price when bid/ask are absent or zero
        if bid <= 0 or ask <= 0:
            if last <= 0:
                raise MarketDataUnavailableError(pair, "no price data from Yahoo Finance")
            bid = last
            ask = last

        return SpotPrice(pair=pair, bid=bid, ask=ask, timestamp=datetime.now(tz=timezone.utc))
    except MarketDataUnavailableError:
        raise
    except Exception as exc:
        raise MarketDataUnavailableError(pair, str(exc)) from exc


class YahooFinanceProvider(MarketDataProvider):
    """Fetches live FX spot prices from Yahoo Finance via yfinance."""

    def __init__(self, timeout: int = 5) -> None:
        self._timeout = timeout

    async def get_spot(self, pair: str) -> SpotPrice:
        ticker_symbol = _PAIR_TO_TICKER.get(pair)
        if ticker_symbol is None:
            raise MarketDataUnavailableError(pair, f"no Yahoo Finance ticker mapping for {pair!r}")
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _fetch_sync, pair, ticker_symbol, self._timeout)

    async def get_spots(self, pairs: list[str]) -> dict[str, SpotPrice]:
        results = await asyncio.gather(
            *[self.get_spot(p) for p in pairs],
            return_exceptions=True,
        )
        return {
            pair: result
            for pair, result in zip(pairs, results)
            if isinstance(result, SpotPrice)
        }
