"""Unit tests for app.domain.calendar — G10 market calendars."""

from datetime import date

import pytest

from app.domain.calendar import (
    CombinedCalendar,
    MarketCalendar,
    add_business_days,
    get_calendar,
    next_business_day,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def bd(currency: str, d: date) -> bool:
    return get_calendar(currency).is_business_day(d)


# ---------------------------------------------------------------------------
# USD / FED
# ---------------------------------------------------------------------------

class TestUSD:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("USD", date(2026, 1, 1))

    def test_independence_day_is_holiday(self) -> None:
        assert not bd("USD", date(2026, 7, 4))

    def test_thanksgiving_is_holiday(self) -> None:
        # 4th Thursday of November 2026 = Nov 26
        assert not bd("USD", date(2026, 11, 26))

    def test_day_after_thanksgiving_is_holiday(self) -> None:
        assert not bd("USD", date(2026, 11, 27))

    def test_labor_day_is_holiday(self) -> None:
        # 1st Monday of September 2026 = Sep 7
        assert not bd("USD", date(2026, 9, 7))

    def test_memorial_day_is_holiday(self) -> None:
        # Last Monday of May 2026 = May 25
        assert not bd("USD", date(2026, 5, 25))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("USD", date(2026, 12, 25))

    def test_good_friday_is_holiday(self) -> None:
        # Good Friday 2026 = Apr 3
        assert not bd("USD", date(2026, 4, 3))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("USD", date(2026, 3, 16))  # Monday, no holiday

    def test_mlk_day_is_holiday(self) -> None:
        # 3rd Monday of January 2026 = Jan 19
        assert not bd("USD", date(2026, 1, 19))

    def test_juneteenth_is_holiday(self) -> None:
        assert not bd("USD", date(2026, 6, 19))


# ---------------------------------------------------------------------------
# EUR / ECB TARGET
# ---------------------------------------------------------------------------

class TestEUR:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("EUR", date(2026, 1, 1))

    def test_good_friday_is_holiday(self) -> None:
        assert not bd("EUR", date(2026, 4, 3))

    def test_easter_monday_is_holiday(self) -> None:
        assert not bd("EUR", date(2026, 4, 6))

    def test_labour_day_is_holiday(self) -> None:
        assert not bd("EUR", date(2026, 5, 1))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("EUR", date(2026, 12, 25))

    def test_boxing_day_is_holiday(self) -> None:
        assert not bd("EUR", date(2026, 12, 26))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("EUR", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# GBP / BOE
# ---------------------------------------------------------------------------

class TestGBP:
    def test_good_friday_is_holiday(self) -> None:
        assert not bd("GBP", date(2026, 4, 3))

    def test_early_may_bank_holiday(self) -> None:
        # 1st Monday of May 2026 = May 4
        assert not bd("GBP", date(2026, 5, 4))

    def test_boxing_day_is_holiday(self) -> None:
        assert not bd("GBP", date(2026, 12, 26))

    def test_summer_bank_holiday(self) -> None:
        # Last Monday of August 2026 = Aug 31
        assert not bd("GBP", date(2026, 8, 31))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("GBP", date(2026, 3, 17))


# ---------------------------------------------------------------------------
# JPY / BOJ
# ---------------------------------------------------------------------------

class TestJPY:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("JPY", date(2026, 1, 1))

    def test_bank_holiday_jan2_is_holiday(self) -> None:
        assert not bd("JPY", date(2026, 1, 2))

    def test_bank_holiday_jan3_is_holiday(self) -> None:
        assert not bd("JPY", date(2026, 1, 3))

    def test_coming_of_age_day(self) -> None:
        # 2nd Monday of January 2026 = Jan 12
        assert not bd("JPY", date(2026, 1, 12))

    def test_marine_day(self) -> None:
        # 3rd Monday of July 2026 = Jul 20
        assert not bd("JPY", date(2026, 7, 20))

    def test_mountain_day_is_holiday(self) -> None:
        assert not bd("JPY", date(2026, 8, 11))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("JPY", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# CHF / SNB
# ---------------------------------------------------------------------------

class TestCHF:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("CHF", date(2026, 1, 1))

    def test_berchtoldstag_is_holiday(self) -> None:
        assert not bd("CHF", date(2026, 1, 2))

    def test_national_day_is_holiday(self) -> None:
        assert not bd("CHF", date(2026, 8, 1))

    def test_good_friday_is_holiday(self) -> None:
        assert not bd("CHF", date(2026, 4, 3))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("CHF", date(2026, 12, 25))

    def test_st_stephens_is_holiday(self) -> None:
        assert not bd("CHF", date(2026, 12, 26))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("CHF", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# CAD / Bank of Canada
# ---------------------------------------------------------------------------

class TestCAD:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("CAD", date(2026, 1, 1))

    def test_canada_day_is_holiday(self) -> None:
        assert not bd("CAD", date(2026, 7, 1))

    def test_thanksgiving_is_holiday(self) -> None:
        # 2nd Monday of October 2026 = Oct 12
        assert not bd("CAD", date(2026, 10, 12))

    def test_labour_day_is_holiday(self) -> None:
        # 1st Monday of September 2026 = Sep 7
        assert not bd("CAD", date(2026, 9, 7))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("CAD", date(2026, 12, 25))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("CAD", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# AUD / RBA
# ---------------------------------------------------------------------------

class TestAUD:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("AUD", date(2026, 1, 1))

    def test_australia_day_is_holiday(self) -> None:
        assert not bd("AUD", date(2026, 1, 26))

    def test_anzac_day_is_holiday(self) -> None:
        assert not bd("AUD", date(2026, 4, 25))

    def test_good_friday_is_holiday(self) -> None:
        assert not bd("AUD", date(2026, 4, 3))

    def test_queens_birthday_is_holiday(self) -> None:
        # 2nd Monday of June 2026 = Jun 8
        assert not bd("AUD", date(2026, 6, 8))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("AUD", date(2026, 12, 25))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("AUD", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# NZD / RBNZ
# ---------------------------------------------------------------------------

class TestNZD:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("NZD", date(2026, 1, 1))

    def test_waitangi_day_is_holiday(self) -> None:
        assert not bd("NZD", date(2026, 2, 6))

    def test_anzac_day_is_holiday(self) -> None:
        assert not bd("NZD", date(2026, 4, 25))

    def test_good_friday_is_holiday(self) -> None:
        assert not bd("NZD", date(2026, 4, 3))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("NZD", date(2026, 12, 25))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("NZD", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# SEK / Riksbank
# ---------------------------------------------------------------------------

class TestSEK:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("SEK", date(2026, 1, 1))

    def test_national_day_is_holiday(self) -> None:
        assert not bd("SEK", date(2026, 6, 6))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("SEK", date(2026, 12, 25))

    def test_epiphany_is_holiday(self) -> None:
        assert not bd("SEK", date(2026, 1, 6))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("SEK", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# NOK / Norges Bank
# ---------------------------------------------------------------------------

class TestNOK:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("NOK", date(2026, 1, 1))

    def test_constitution_day_is_holiday(self) -> None:
        assert not bd("NOK", date(2026, 5, 17))

    def test_labour_day_is_holiday(self) -> None:
        assert not bd("NOK", date(2026, 5, 1))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("NOK", date(2026, 12, 25))

    def test_good_friday_is_holiday(self) -> None:
        assert not bd("NOK", date(2026, 4, 3))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("NOK", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# DKK / Danmarks Nationalbank
# ---------------------------------------------------------------------------

class TestDKK:
    def test_new_year_is_holiday(self) -> None:
        assert not bd("DKK", date(2026, 1, 1))

    def test_constitution_day_is_holiday(self) -> None:
        assert not bd("DKK", date(2026, 6, 5))

    def test_christmas_is_holiday(self) -> None:
        assert not bd("DKK", date(2026, 12, 25))

    def test_maundy_thursday_is_holiday(self) -> None:
        # Maundy Thursday 2026 = Apr 2
        assert not bd("DKK", date(2026, 4, 2))

    def test_normal_weekday_is_business_day(self) -> None:
        assert bd("DKK", date(2026, 3, 16))


# ---------------------------------------------------------------------------
# Weekends — all currencies
# ---------------------------------------------------------------------------

_ALL_G10 = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "SEK", "NOK", "DKK"]


@pytest.mark.parametrize("ccy", _ALL_G10)
def test_saturday_is_not_business_day(ccy: str) -> None:
    assert not bd(ccy, date(2026, 3, 14))  # Saturday


@pytest.mark.parametrize("ccy", _ALL_G10)
def test_sunday_is_not_business_day(ccy: str) -> None:
    assert not bd(ccy, date(2026, 3, 15))  # Sunday


# ---------------------------------------------------------------------------
# CombinedCalendar
# ---------------------------------------------------------------------------

class TestCombinedCalendar:
    def test_holiday_in_either_calendar_is_excluded(self) -> None:
        usd = get_calendar("USD")
        eur = get_calendar("EUR")
        combined = CombinedCalendar(usd, eur)
        # Jul 4 is USD holiday but not EUR
        assert not combined.is_business_day(date(2026, 7, 4))
        # May 1 is EUR holiday but not USD
        assert not combined.is_business_day(date(2026, 5, 1))

    def test_common_business_day_is_open(self) -> None:
        usd = get_calendar("USD")
        eur = get_calendar("EUR")
        combined = CombinedCalendar(usd, eur)
        assert combined.is_business_day(date(2026, 3, 16))

    def test_name_combines_calendars(self) -> None:
        combined = CombinedCalendar(get_calendar("USD"), get_calendar("EUR"))
        assert "USD" in combined.name
        assert "EUR" in combined.name


# ---------------------------------------------------------------------------
# add_business_days
# ---------------------------------------------------------------------------

class TestAddBusinessDays:
    def test_add_two_biz_days_over_holiday_and_weekend(self) -> None:
        # May 22 (Fri) + 2 USD biz days:
        #   skip Sat/Sun → May 25 = Memorial Day (holiday, skip) → May 26 (biz 1) → May 27 (biz 2)
        # Note: work item spec said May 26 but did not account for Memorial Day on May 25.
        usd = get_calendar("USD")
        result = add_business_days(date(2026, 5, 22), 2, usd)
        assert result == date(2026, 5, 27)

    def test_zero_days_returns_same(self) -> None:
        usd = get_calendar("USD")
        d = date(2026, 3, 16)
        assert add_business_days(d, 0, usd) == d

    def test_negative_days(self) -> None:
        usd = get_calendar("USD")
        # Mar 18 (Wed) - 1 biz day = Mar 17 (Tue)
        assert add_business_days(date(2026, 3, 18), -1, usd) == date(2026, 3, 17)

    def test_skips_weekend(self) -> None:
        usd = get_calendar("USD")
        # Mar 13 (Fri) + 1 = Mar 16 (Mon, skipping Sat/Sun)
        assert add_business_days(date(2026, 3, 13), 1, usd) == date(2026, 3, 16)


# ---------------------------------------------------------------------------
# next_business_day
# ---------------------------------------------------------------------------

class TestNextBusinessDay:
    def test_next_day_from_weekday(self) -> None:
        usd = get_calendar("USD")
        assert next_business_day(date(2026, 3, 16), usd) == date(2026, 3, 17)

    def test_skips_weekend(self) -> None:
        usd = get_calendar("USD")
        # Friday → Monday
        assert next_business_day(date(2026, 3, 13), usd) == date(2026, 3, 16)

    def test_skips_holiday(self) -> None:
        usd = get_calendar("USD")
        # Dec 24 (Thu) + next biz day = Dec 28 (Mon) since Dec 25=Xmas
        result = next_business_day(date(2026, 12, 24), usd)
        assert result == date(2026, 12, 28)


# ---------------------------------------------------------------------------
# get_calendar errors
# ---------------------------------------------------------------------------

def test_unknown_currency_raises() -> None:
    with pytest.raises(ValueError, match="No market calendar"):
        get_calendar("XYZ")


def test_get_calendar_accepts_string() -> None:
    cal = get_calendar("usd")
    assert isinstance(cal, MarketCalendar)


def test_get_calendar_accepts_currency_enum() -> None:
    from app.domain.types import Currency
    cal = get_calendar(Currency.EUR)
    assert isinstance(cal, MarketCalendar)


# ---------------------------------------------------------------------------
# Holiday caching
# ---------------------------------------------------------------------------

def test_holidays_are_cached() -> None:
    cal = get_calendar("USD")
    h1 = cal.holidays(2026)
    h2 = cal.holidays(2026)
    assert h1 is h2  # same frozenset object
