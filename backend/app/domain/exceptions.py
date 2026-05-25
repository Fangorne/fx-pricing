"""Domain exceptions for the FX Pricing platform."""

from __future__ import annotations


class FXDomainError(Exception):
    """Base class for all FX domain exceptions."""


class UnsupportedCurrencyPairError(FXDomainError):
    """Raised when a currency pair has no registered convention."""

    def __init__(self, pair: str) -> None:
        self.pair = pair
        super().__init__(f"No FX convention registered for pair {pair!r}")


class MarketDataUnavailableError(FXDomainError):
    """Raised when a market data provider cannot return a price."""

    def __init__(self, pair: str, reason: str = "") -> None:
        self.pair = pair
        msg = f"Market data unavailable for {pair!r}"
        if reason:
            msg += f": {reason}"
        super().__init__(msg)


class StaleMarketDataError(FXDomainError):
    """Raised when cached market data exceeds the staleness threshold."""

    def __init__(self, pair: str, age_seconds: float, threshold: int) -> None:
        self.pair = pair
        self.age_seconds = age_seconds
        self.threshold = threshold
        super().__init__(
            f"Market data for {pair!r} is stale: "
            f"{age_seconds:.0f}s old (threshold: {threshold}s)"
        )
