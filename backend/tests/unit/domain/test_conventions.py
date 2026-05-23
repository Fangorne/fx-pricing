"""Unit tests for app.domain.conventions — FX convention registry."""

import pytest

from app.domain.business_day import BusinessDayConvention
from app.domain.conventions import FX_CONVENTIONS, DayCountBasis, FXConvention, get_convention
from app.domain.exceptions import UnsupportedCurrencyPairError
from app.domain.types import Currency, CurrencyPair, QuotationSide

# ---------------------------------------------------------------------------
# DayCountBasis
# ---------------------------------------------------------------------------

class TestDayCountBasis:
    def test_act_360_str(self) -> None:
        assert str(DayCountBasis.ACT_360) == "Act/360"

    def test_act_365_str(self) -> None:
        assert str(DayCountBasis.ACT_365) == "Act/365"

    def test_act_act_str(self) -> None:
        assert str(DayCountBasis.ACT_ACT) == "Act/Act"

    def test_three_variants_defined(self) -> None:
        assert len(DayCountBasis) == 3


# ---------------------------------------------------------------------------
# FXConvention dataclass
# ---------------------------------------------------------------------------

class TestFXConvention:
    def test_frozen(self) -> None:
        conv = get_convention("EUR/USD")
        with pytest.raises(Exception):
            conv.spot_lag = 99  # type: ignore[misc]

    def test_hashable(self) -> None:
        conv = get_convention("EUR/USD")
        assert hash(conv) == hash(get_convention("EUR/USD"))

    def test_equality(self) -> None:
        assert get_convention("EUR/USD") == get_convention("EUR/USD")
        assert get_convention("EUR/USD") != get_convention("USD/JPY")


# ---------------------------------------------------------------------------
# Acceptance criteria — specific pairs
# ---------------------------------------------------------------------------

class TestAcceptanceCriteria:
    def test_eurusd(self) -> None:
        c = get_convention("EUR/USD")
        assert c.spot_lag == 2
        assert c.day_count == DayCountBasis.ACT_360
        assert c.roll_convention == BusinessDayConvention.MODIFIED_FOLLOWING
        assert c.pip_precision == 4
        assert c.quotation_side == QuotationSide.DIRECT

    def test_usdjpy(self) -> None:
        c = get_convention("USD/JPY")
        assert c.spot_lag == 2
        assert c.pip_precision == 2

    def test_usdcad(self) -> None:
        c = get_convention("USD/CAD")
        assert c.spot_lag == 1
        assert c.day_count == DayCountBasis.ACT_365

    def test_gbpusd(self) -> None:
        c = get_convention("GBP/USD")
        assert c.spot_lag == 2
        assert c.day_count == DayCountBasis.ACT_365
        assert c.pip_precision == 4

    def test_eurjpy(self) -> None:
        c = get_convention("EUR/JPY")
        assert c.pip_precision == 2

    def test_usdchf(self) -> None:
        c = get_convention("USD/CHF")
        assert c.spot_lag == 2
        assert c.day_count == DayCountBasis.ACT_360

    def test_audusd(self) -> None:
        c = get_convention("AUD/USD")
        assert c.spot_lag == 2
        assert c.day_count == DayCountBasis.ACT_365

    def test_nzdusd(self) -> None:
        c = get_convention("NZD/USD")
        assert c.spot_lag == 2


# ---------------------------------------------------------------------------
# All 12 G10 pairs present in registry
# ---------------------------------------------------------------------------

_REQUIRED_PAIRS = [
    "EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "USD/CAD",
    "AUD/USD", "NZD/USD", "EUR/GBP", "EUR/JPY", "EUR/CHF",
    "GBP/JPY", "AUD/JPY",
]


@pytest.mark.parametrize("pair", _REQUIRED_PAIRS)
def test_all_g10_pairs_in_registry(pair: str) -> None:
    assert pair in FX_CONVENTIONS


@pytest.mark.parametrize("pair", _REQUIRED_PAIRS)
def test_all_pairs_have_valid_convention(pair: str) -> None:
    c = get_convention(pair)
    assert isinstance(c, FXConvention)
    assert c.spot_lag in (1, 2)
    assert isinstance(c.day_count, DayCountBasis)
    assert isinstance(c.roll_convention, BusinessDayConvention)
    assert c.pip_precision in (2, 4)
    assert isinstance(c.quotation_side, QuotationSide)


# ---------------------------------------------------------------------------
# get_convention — input format flexibility
# ---------------------------------------------------------------------------

class TestGetConventionInputFormats:
    def test_slash_string(self) -> None:
        assert get_convention("EUR/USD").spot_lag == 2

    def test_six_char_string(self) -> None:
        assert get_convention("EURUSD").spot_lag == 2

    def test_lowercase(self) -> None:
        assert get_convention("eur/usd").spot_lag == 2

    def test_currency_pair_object(self) -> None:
        pair = CurrencyPair(Currency.EUR, Currency.USD)
        assert get_convention(pair).spot_lag == 2

    def test_unknown_pair_raises(self) -> None:
        with pytest.raises(UnsupportedCurrencyPairError) as exc_info:
            get_convention("EUR/SEK")
        assert "EUR/SEK" in str(exc_info.value)

    def test_unknown_pair_has_pair_attribute(self) -> None:
        with pytest.raises(UnsupportedCurrencyPairError) as exc_info:
            get_convention("XXX/YYY")
        assert exc_info.value.pair == "XXX/YYY"


# ---------------------------------------------------------------------------
# UnsupportedCurrencyPairError
# ---------------------------------------------------------------------------

class TestUnsupportedCurrencyPairError:
    def test_is_fx_domain_error(self) -> None:
        from app.domain.exceptions import FXDomainError
        err = UnsupportedCurrencyPairError("EUR/SEK")
        assert isinstance(err, FXDomainError)

    def test_message_contains_pair(self) -> None:
        err = UnsupportedCurrencyPairError("EUR/SEK")
        assert "EUR/SEK" in str(err)

    def test_pair_attribute(self) -> None:
        err = UnsupportedCurrencyPairError("EUR/SEK")
        assert err.pair == "EUR/SEK"


# ---------------------------------------------------------------------------
# Spot lag consistency with SPOT_LAGS in date_generation
# ---------------------------------------------------------------------------

def test_usdcad_spot_lag_consistent_with_date_generation() -> None:
    from app.domain.date_generation import SPOT_LAGS
    conv = get_convention("USD/CAD")
    assert conv.spot_lag == SPOT_LAGS["USD/CAD"]


def test_eurusd_spot_lag_consistent_with_date_generation() -> None:
    from app.domain.date_generation import SPOT_LAGS
    conv = get_convention("EUR/USD")
    # EUR/USD not in SPOT_LAGS → default T+2
    assert "EUR/USD" not in SPOT_LAGS
    assert conv.spot_lag == 2
