"""Market data domain types — SpotPrice and related value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class SpotPrice:
    """A live FX spot price with bid/ask spread and timestamp.

    All prices are in units of the quote currency per unit of base currency.
    Timestamp must be timezone-aware UTC.
    """

    pair: str
    bid: float
    ask: float
    timestamp: datetime

    def __post_init__(self) -> None:
        if self.bid <= 0 or self.ask <= 0:
            raise ValueError(f"bid and ask must be positive, got bid={self.bid} ask={self.ask}")
        if self.bid > self.ask:
            raise ValueError(f"bid ({self.bid}) must be <= ask ({self.ask})")
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware (UTC)")

    @property
    def mid(self) -> float:
        """Mid price: arithmetic mean of bid and ask."""
        return (self.bid + self.ask) / 2

    def is_stale(self, max_age_seconds: int) -> bool:
        """Return True if the price is older than max_age_seconds."""
        now = datetime.now(tz=timezone.utc)
        age = (now - self.timestamp).total_seconds()
        return age > max_age_seconds

    @property
    def spread(self) -> float:
        """Bid-ask spread."""
        return self.ask - self.bid
