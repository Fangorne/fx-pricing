"""FX domain value objects — Currency, CurrencyPair, Tenor, QuotationSide."""

from __future__ import annotations

import enum
from dataclasses import dataclass


class Currency(enum.StrEnum):
    """ISO 4217 currency codes for G10 FX market."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"
    CAD = "CAD"
    AUD = "AUD"
    NZD = "NZD"
    SEK = "SEK"
    NOK = "NOK"
    DKK = "DKK"



class QuotationSide(enum.Enum):
    """FX quotation convention.

    DIRECT: 1 unit of base currency = X units of quote currency (e.g. EUR/USD = 1.08)
    INDIRECT: 1 unit of quote currency = X units of base currency (e.g. USD/JPY = 155)
    """

    DIRECT = "direct"
    INDIRECT = "indirect"


@dataclass(frozen=True)
class CurrencyPair:
    """An ordered FX currency pair (base / quote).

    Examples
    --------
    >>> CurrencyPair(Currency.EUR, Currency.USD)
    CurrencyPair(base=<Currency.EUR: 'EUR'>, quote=<Currency.USD: 'USD'>)
    """

    base: Currency
    quote: Currency

    def __post_init__(self) -> None:
        if self.base == self.quote:
            raise ValueError(f"Base and quote currencies must differ, got {self.base}/{self.quote}")

    def __str__(self) -> str:
        return f"{self.base}/{self.quote}"

    @classmethod
    def from_string(cls, value: str) -> CurrencyPair:
        """Parse "EURUSD" or "EUR/USD" into a CurrencyPair."""
        cleaned = value.strip().upper().replace("/", "")
        if len(cleaned) != 6:  # noqa: PLR2004
            raise ValueError(f"Cannot parse currency pair from {value!r}: expected 6-char code")
        base = Currency(cleaned[:3])
        quote = Currency(cleaned[3:])
        return cls(base=base, quote=quote)


# Approximate calendar-day counts per tenor label.
# ON=1, TN=2, SN=3 follow T+1/T+2/T+3 spot conventions.
# Month/year values are conventional approximations used for risk bucketing.
_TENOR_DAYS: dict[str, int] = {
    "ON": 1,
    "TN": 2,
    "SN": 3,
    "1W": 7,
    "2W": 14,
    "1M": 30,
    "2M": 61,
    "3M": 91,
    "6M": 182,
    "9M": 274,
    "12M": 365,
    "1Y": 365,
    "2Y": 730,
}


@dataclass(frozen=True)
class Tenor:
    """An FX tenor label (e.g. ON, 1W, 3M, 1Y) with approximate day count."""

    label: str

    def __post_init__(self) -> None:
        if self.label not in _TENOR_DAYS:
            raise ValueError(
                f"Unsupported tenor {self.label!r}. "
                f"Valid tenors: {', '.join(_TENOR_DAYS)}"
            )

    def __str__(self) -> str:
        return self.label

    def to_days(self) -> int:
        """Return approximate calendar-day count for this tenor."""
        return _TENOR_DAYS[self.label]

    @classmethod
    def from_string(cls, value: str) -> Tenor:
        """Parse a tenor label, normalising case."""
        return cls(label=value.strip().upper())
