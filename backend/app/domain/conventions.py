"""FX convention registry — market conventions for G10 currency pairs."""

from __future__ import annotations

import enum
from dataclasses import dataclass

from app.domain.business_day import BusinessDayConvention
from app.domain.exceptions import UnsupportedCurrencyPairError
from app.domain.types import CurrencyPair, QuotationSide


class DayCountBasis(enum.Enum):
    """Day count basis used for interest rate and FX forward calculations."""

    ACT_360 = "Act/360"
    ACT_365 = "Act/365"
    ACT_ACT = "Act/Act"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class FXConvention:
    """Market conventions for a specific FX currency pair.

    Encapsulates settlement, pricing, and quotation conventions
    needed by the pricing engine and date generation layer.
    """

    spot_lag: int
    day_count: DayCountBasis
    roll_convention: BusinessDayConvention
    pip_precision: int
    quotation_side: QuotationSide


def _conv(
    spot_lag: int,
    day_count: DayCountBasis,
    pip_precision: int,
    quotation_side: QuotationSide,
    roll_convention: BusinessDayConvention = BusinessDayConvention.MODIFIED_FOLLOWING,
) -> FXConvention:
    return FXConvention(
        spot_lag=spot_lag,
        day_count=day_count,
        roll_convention=roll_convention,
        pip_precision=pip_precision,
        quotation_side=quotation_side,
    )


_D = QuotationSide.DIRECT
_I = QuotationSide.INDIRECT
_360 = DayCountBasis.ACT_360
_365 = DayCountBasis.ACT_365

# Registry keyed by canonical "BASE/QUOTE" string.
# All pairs listed in both directions for symmetric lookup where applicable.
FX_CONVENTIONS: dict[str, FXConvention] = {
    # Major USD pairs
    "EUR/USD": _conv(2, _360, 4, _D),
    "USD/JPY": _conv(2, _360, 2, _I),
    "GBP/USD": _conv(2, _365, 4, _D),
    "USD/CHF": _conv(2, _360, 4, _I),
    "USD/CAD": _conv(1, _365, 4, _I),
    "AUD/USD": _conv(2, _365, 4, _D),
    "NZD/USD": _conv(2, _365, 4, _D),
    # EUR crosses
    "EUR/GBP": _conv(2, _360, 4, _D),
    "EUR/JPY": _conv(2, _360, 2, _D),
    "EUR/CHF": _conv(2, _360, 4, _D),
    # Other crosses
    "GBP/JPY": _conv(2, _365, 2, _D),
    "AUD/JPY": _conv(2, _365, 2, _D),
}


def get_convention(pair: CurrencyPair | str) -> FXConvention:
    """Return the FXConvention for the given currency pair.

    Accepts a CurrencyPair, a slash-string "EUR/USD", or a 6-char "EURUSD".
    Raises UnsupportedCurrencyPairError for unregistered pairs.
    """
    if isinstance(pair, CurrencyPair):
        key = str(pair)
    else:
        s = pair.strip().upper()
        if "/" not in s and len(s) == 6:  # noqa: PLR2004
            key = f"{s[:3]}/{s[3:]}"
        else:
            key = s

    try:
        return FX_CONVENTIONS[key]
    except KeyError:
        raise UnsupportedCurrencyPairError(key) from None
