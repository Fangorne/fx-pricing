"""Abstract base class for market data providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.market_data import SpotPrice


class MarketDataProvider(ABC):
    """Interface for fetching live FX spot prices."""

    @abstractmethod
    async def get_spot(self, pair: str) -> SpotPrice:
        """Fetch the current spot price for a currency pair.

        Raises:
            MarketDataUnavailableError: if the provider cannot return a price.
        """

    @abstractmethod
    async def get_spots(self, pairs: list[str]) -> dict[str, SpotPrice]:
        """Fetch spot prices for multiple currency pairs.

        Returns a dict keyed by pair string. Pairs that fail are omitted.
        """
