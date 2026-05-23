"""Domain exceptions for the FX Pricing platform."""

from __future__ import annotations


class FXDomainError(Exception):
    """Base class for all FX domain exceptions."""


class UnsupportedCurrencyPairError(FXDomainError):
    """Raised when a currency pair has no registered convention."""

    def __init__(self, pair: str) -> None:
        self.pair = pair
        super().__init__(f"No FX convention registered for pair {pair!r}")
