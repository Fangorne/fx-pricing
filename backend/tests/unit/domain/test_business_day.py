"""Unit tests for app.domain.business_day — adjustment conventions."""

from datetime import date

import pytest

from app.domain.business_day import BusinessDayConvention, adjust
from app.domain.calendar import get_calendar

F = BusinessDayConvention.FOLLOWING
MF = BusinessDayConvention.MODIFIED_FOLLOWING
P = BusinessDayConvention.PRECEDING
MP = BusinessDayConvention.MODIFIED_PRECEDING
EOM = BusinessDayConvention.END_OF_MONTH

USD = get_calendar("USD")
EUR = get_calendar("EUR")


# ---------------------------------------------------------------------------
# FOLLOWING
# ---------------------------------------------------------------------------

class TestFollowing:
    def test_holiday_on_friday_advances_to_monday(self) -> None:
        # Good Friday 2026 = Apr 3 (Friday, USD holiday) → Apr 6 (Monday)
        assert adjust(date(2026, 4, 3), F, USD) == date(2026, 4, 6)

    def test_saturday_advances_to_monday(self) -> None:
        # Mar 14 2026 = Saturday → Mar 16 (Monday)
        assert adjust(date(2026, 3, 14), F, USD) == date(2026, 3, 16)

    def test_sunday_advances_to_monday(self) -> None:
        # Mar 15 2026 = Sunday → Mar 16 (Monday)
        assert adjust(date(2026, 3, 15), F, USD) == date(2026, 3, 16)

    def test_holiday_advances_past_holiday(self) -> None:
        # Jul 4 2026 = Saturday (Independence Day observed Fri Jul 3)
        # Jul 3 2026 = Friday (observed holiday) → Jul 6 (Monday)
        assert adjust(date(2026, 7, 3), F, USD) == date(2026, 7, 6)

    def test_can_cross_month_boundary(self) -> None:
        # Apr 30 2026 = Thursday, IS a business day; Apr 31 doesn't exist.
        # Use a date that crosses: Apr 30 + Following should stay Apr 30 (BD already).
        # Let's use a weekend at month end that crosses: Sep 30 2026 = Wednesday (BD) — skip.
        # Oct 31 2026 = Saturday → Nov 2 (Monday, crossing month)
        assert adjust(date(2026, 10, 31), F, USD) == date(2026, 11, 2)

    def test_already_business_day_unchanged(self) -> None:
        assert adjust(date(2026, 3, 16), F, USD) == date(2026, 3, 16)


# ---------------------------------------------------------------------------
# MODIFIED FOLLOWING
# ---------------------------------------------------------------------------

class TestModifiedFollowing:
    def test_stays_in_month_when_following_would_cross(self) -> None:
        # Mar 31 2026 = Tuesday — already a BD; use a month-end that falls on weekend.
        # Jan 31 2026 = Saturday → Following = Feb 2 (Mon, crosses Jan) → MF = Jan 30 (Fri)
        assert adjust(date(2026, 1, 31), MF, USD) == date(2026, 1, 30)

    def test_advances_when_same_month(self) -> None:
        # Mar 14 2026 = Saturday → Following = Mar 16 (Mon, same month) → MF = Mar 16
        assert adjust(date(2026, 3, 14), MF, USD) == date(2026, 3, 16)

    def test_acceptance_criterion_mar31_sunday(self) -> None:
        # Mar 31 2024 = Sunday → Following = Apr 1 (crosses month) → MF = last BD of Mar
        # Mar 29 2024 = Good Friday (USD holiday), Mar 30 = Saturday → last BD = Mar 28 (Thu)
        usd_2024 = get_calendar("USD")
        assert adjust(date(2024, 3, 31), MF, usd_2024) == date(2024, 3, 28)

    def test_acceptance_criterion_apr30_already_bd(self) -> None:
        # Apr 30 2026 = Thursday = BD → MF returns it unchanged
        assert adjust(date(2026, 4, 30), MF, USD) == date(2026, 4, 30)

    def test_already_business_day_unchanged(self) -> None:
        assert adjust(date(2026, 3, 16), MF, USD) == date(2026, 3, 16)

    def test_eur_calendar(self) -> None:
        # Dec 31 2026 = Thursday = BD → MF returns it unchanged
        assert adjust(date(2026, 12, 31), MF, EUR) == date(2026, 12, 31)


# ---------------------------------------------------------------------------
# PRECEDING
# ---------------------------------------------------------------------------

class TestPreceding:
    def test_saturday_goes_to_friday(self) -> None:
        # Mar 14 2026 = Saturday → Mar 13 (Friday)
        assert adjust(date(2026, 3, 14), P, USD) == date(2026, 3, 13)

    def test_sunday_goes_to_friday(self) -> None:
        # Mar 15 2026 = Sunday → Mar 13 (Friday)
        assert adjust(date(2026, 3, 15), P, USD) == date(2026, 3, 13)

    def test_holiday_goes_to_previous_bd(self) -> None:
        # Jan 1 2026 = Thursday (New Year) → Dec 31 2025 (Wednesday)
        assert adjust(date(2026, 1, 1), P, USD) == date(2025, 12, 31)

    def test_can_cross_month_boundary(self) -> None:
        # Nov 1 2026 = Sunday → Oct 30 2026 (Friday, crossing month)
        assert adjust(date(2026, 11, 1), P, USD) == date(2026, 10, 30)

    def test_already_business_day_unchanged(self) -> None:
        assert adjust(date(2026, 3, 16), P, USD) == date(2026, 3, 16)


# ---------------------------------------------------------------------------
# MODIFIED PRECEDING
# ---------------------------------------------------------------------------

class TestModifiedPreceding:
    def test_stays_in_month_when_preceding_would_cross(self) -> None:
        # Nov 1 2026 = Sunday → Preceding = Oct 30 (crosses Nov) → MP = Nov 2 (Mon, first BD of Nov)
        assert adjust(date(2026, 11, 1), MP, USD) == date(2026, 11, 2)

    def test_goes_back_when_same_month(self) -> None:
        # Mar 15 2026 = Sunday → Preceding = Mar 13 (Fri, same month) → MP = Mar 13
        assert adjust(date(2026, 3, 15), MP, USD) == date(2026, 3, 13)

    def test_already_business_day_unchanged(self) -> None:
        assert adjust(date(2026, 3, 16), MP, USD) == date(2026, 3, 16)

    def test_holiday_at_month_start_stays_in_month(self) -> None:
        # Jan 1 2026 = Thursday (New Year, USD holiday)
        # Preceding = Dec 31 2025 (crosses Jan) → MP = Jan 2 2026 (first BD of Jan)
        assert adjust(date(2026, 1, 1), MP, USD) == date(2026, 1, 2)


# ---------------------------------------------------------------------------
# END OF MONTH
# ---------------------------------------------------------------------------

class TestEndOfMonth:
    def test_returns_last_bd_of_month(self) -> None:
        # Any date in Jan 2026 → last BD = Jan 30 (Fri; Jan 31 = Sat)
        assert adjust(date(2026, 1, 15), EOM, USD) == date(2026, 1, 30)

    def test_last_bd_skips_holiday_at_month_end(self) -> None:
        # Dec 2026: Dec 31 = Thursday (BD), Dec 25 = Fri (Christmas, holiday),
        # Dec 24 = Thursday (BD) ... last BD of Dec 2026 = Dec 31
        assert adjust(date(2026, 12, 1), EOM, USD) == date(2026, 12, 31)

    def test_eom_on_business_day_still_returns_last_bd(self) -> None:
        # EOM ignores whether input is a BD or not — always returns last BD
        assert adjust(date(2026, 3, 16), EOM, USD) == adjust(date(2026, 3, 31), EOM, USD)

    def test_feb_non_leap_year(self) -> None:
        # Feb 2026: Feb 28 = Saturday → last BD = Feb 27 (Friday)
        assert adjust(date(2026, 2, 1), EOM, USD) == date(2026, 2, 27)

    def test_eur_calendar(self) -> None:
        # Apr 2026: Apr 30 = Thursday (BD) → last BD = Apr 30
        assert adjust(date(2026, 4, 15), EOM, EUR) == date(2026, 4, 30)


# ---------------------------------------------------------------------------
# Parametrized: already-BD is a no-op for all non-EOM conventions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("conv", [F, MF, P, MP])
def test_business_day_unchanged_for_all_conventions(conv: BusinessDayConvention) -> None:
    # Mar 16 2026 = Monday, no holiday
    assert adjust(date(2026, 3, 16), conv, USD) == date(2026, 3, 16)


# ---------------------------------------------------------------------------
# Works with any MarketCalendar
# ---------------------------------------------------------------------------

def test_eur_good_friday_following(self: None = None) -> None:
    # Apr 3 2026 = Good Friday (EUR holiday) → Following = Apr 6 (Easter Monday also holiday)
    # → Apr 7 (Tuesday)
    assert adjust(date(2026, 4, 3), F, EUR) == date(2026, 4, 7)


def test_eur_good_friday_preceding(self: None = None) -> None:
    # Apr 3 2026 = Good Friday (EUR holiday) → Preceding = Apr 2 (Thursday)
    assert adjust(date(2026, 4, 3), P, EUR) == date(2026, 4, 2)
