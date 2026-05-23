import pytest

from app.domain.types import Currency, CurrencyPair, QuotationSide, Tenor


class TestCurrency:
    def test_all_g10_currencies_defined(self) -> None:
        expected = {"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "SEK", "NOK", "DKK"}
        actual = {c.value for c in Currency}
        assert expected == actual

    def test_str_returns_code(self) -> None:
        assert str(Currency.EUR) == "EUR"
        assert str(Currency.JPY) == "JPY"

    def test_is_string_compatible(self) -> None:
        assert Currency.USD == "USD"


class TestCurrencyPair:
    def test_basic_construction(self) -> None:
        pair = CurrencyPair(Currency.EUR, Currency.USD)
        assert pair.base == Currency.EUR
        assert pair.quote == Currency.USD

    def test_str_representation(self) -> None:
        assert str(CurrencyPair(Currency.EUR, Currency.USD)) == "EUR/USD"

    def test_same_currency_raises(self) -> None:
        with pytest.raises(ValueError, match="must differ"):
            CurrencyPair(Currency.EUR, Currency.EUR)

    @pytest.mark.parametrize("raw", ["EURUSD", "EUR/USD", "eurusd", "eur/usd"])
    def test_from_string(self, raw: str) -> None:
        pair = CurrencyPair.from_string(raw)
        assert pair.base == Currency.EUR
        assert pair.quote == Currency.USD

    def test_from_string_gbpjpy(self) -> None:
        pair = CurrencyPair.from_string("GBPJPY")
        assert pair.base == Currency.GBP
        assert pair.quote == Currency.JPY

    def test_from_string_invalid_length(self) -> None:
        with pytest.raises(ValueError, match="6-char"):
            CurrencyPair.from_string("EUR")

    def test_from_string_unknown_currency(self) -> None:
        with pytest.raises(ValueError):
            CurrencyPair.from_string("XYZABC")

    def test_frozen(self) -> None:
        pair = CurrencyPair(Currency.EUR, Currency.USD)
        with pytest.raises(Exception):
            pair.base = Currency.GBP  # type: ignore[misc]

    def test_equality(self) -> None:
        assert CurrencyPair(Currency.EUR, Currency.USD) == CurrencyPair(Currency.EUR, Currency.USD)
        assert CurrencyPair(Currency.EUR, Currency.USD) != CurrencyPair(Currency.USD, Currency.EUR)

    def test_hashable(self) -> None:
        pair = CurrencyPair(Currency.EUR, Currency.USD)
        assert hash(pair) == hash(CurrencyPair(Currency.EUR, Currency.USD))


class TestTenor:
    @pytest.mark.parametrize(
        ("label", "expected_days"),
        [
            ("ON", 1),
            ("TN", 2),
            ("SN", 3),
            ("1W", 7),
            ("2W", 14),
            ("1M", 30),
            ("2M", 61),
            ("3M", 91),
            ("6M", 182),
            ("9M", 274),
            ("12M", 365),
            ("1Y", 365),
            ("2Y", 730),
        ],
    )
    def test_to_days(self, label: str, expected_days: int) -> None:
        assert Tenor(label).to_days() == expected_days

    @pytest.mark.parametrize("raw", ["ON", "on", "1W", "3M", "1Y", " 3M "])
    def test_from_string(self, raw: str) -> None:
        tenor = Tenor.from_string(raw)
        assert tenor.label == raw.strip().upper()

    def test_str(self) -> None:
        assert str(Tenor("3M")) == "3M"

    def test_invalid_tenor_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported tenor"):
            Tenor("99X")

    def test_frozen(self) -> None:
        t = Tenor("1M")
        with pytest.raises(Exception):
            t.label = "3M"  # type: ignore[misc]

    def test_hashable(self) -> None:
        assert hash(Tenor("1Y")) == hash(Tenor("1Y"))


class TestQuotationSide:
    def test_direct_defined(self) -> None:
        assert QuotationSide.DIRECT.value == "direct"

    def test_indirect_defined(self) -> None:
        assert QuotationSide.INDIRECT.value == "indirect"

    def test_only_two_sides(self) -> None:
        assert len(QuotationSide) == 2
