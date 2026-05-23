"""FX market calendars — business day rules for G10 currencies."""

from __future__ import annotations

import calendar as _cal
from collections.abc import Callable
from datetime import date, timedelta

from app.domain.types import Currency

# ---------------------------------------------------------------------------
# Easter (Meeus/Jones/Butcher algorithm) — no external dependency
# ---------------------------------------------------------------------------

def _easter(year: int) -> date:
    """Return Easter Sunday for the given year (Gregorian calendar)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    ll = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * ll) // 451
    month = (h + ll - 7 * m + 114) // 31
    day = ((h + ll - 7 * m + 114) % 31) + 1
    return date(year, month, day)


# ---------------------------------------------------------------------------
# Helpers for rule-based holidays
# ---------------------------------------------------------------------------

def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """Return the n-th occurrence (1-based) of weekday (Mon=0…Sun=6) in month/year."""
    weeks = _cal.monthcalendar(year, month)
    count = 0
    for week in weeks:
        if week[weekday] != 0:
            count += 1
            if count == n:
                return date(year, month, week[weekday])
    raise ValueError(f"No {n}th weekday={weekday} in {year}-{month:02d}")


def _last_weekday(year: int, month: int, weekday: int) -> date:
    """Return the last occurrence of weekday in month/year."""
    weeks = _cal.monthcalendar(year, month)
    for week in reversed(weeks):
        if week[weekday] != 0:
            return date(year, month, week[weekday])
    raise ValueError(f"No weekday={weekday} in {year}-{month:02d}")


def _observed(d: date) -> date:
    """Return the observed date when a fixed holiday lands on a weekend.

    Saturday → previous Friday; Sunday → next Monday.
    """
    if d.weekday() == 5:  # Saturday
        return d - timedelta(days=1)
    if d.weekday() == 6:  # Sunday
        return d + timedelta(days=1)
    return d


# ---------------------------------------------------------------------------
# HolidayRule type and MarketCalendar
# ---------------------------------------------------------------------------

HolidayRule = Callable[[int], set[date]]


class MarketCalendar:
    """A market calendar for a single currency/financial centre.

    Holidays are computed lazily per year and cached.
    Weekend days default to Saturday and Sunday.
    """

    def __init__(
        self,
        name: str,
        rules: list[HolidayRule],
        weekend_days: frozenset[int] = frozenset({5, 6}),  # Mon=0…Sun=6
    ) -> None:
        self.name = name
        self._rules = rules
        self._weekend_days = weekend_days
        self._cache: dict[int, frozenset[date]] = {}

    def holidays(self, year: int) -> frozenset[date]:
        """Return all holidays for the given year."""
        if year not in self._cache:
            result: set[date] = set()
            for rule in self._rules:
                result |= rule(year)
            self._cache[year] = frozenset(result)
        return self._cache[year]

    def is_business_day(self, d: date) -> bool:
        """Return True if d is a business day (not weekend, not holiday)."""
        if d.weekday() in self._weekend_days:
            return False
        return d not in self.holidays(d.year)

    def next_business_day(self, d: date) -> date:
        """Return the next business day strictly after d."""
        candidate = d + timedelta(days=1)
        while not self.is_business_day(candidate):
            candidate += timedelta(days=1)
        return candidate

    def add_business_days(self, d: date, n: int) -> date:
        """Return the date n business days after d (n may be 0 or negative)."""
        if n == 0:
            return d
        step = timedelta(days=1) if n > 0 else timedelta(days=-1)
        remaining = abs(n)
        current = d
        while remaining > 0:
            current += step
            if self.is_business_day(current):
                remaining -= 1
        return current


class CombinedCalendar(MarketCalendar):
    """A calendar whose holidays are the union of two or more calendars."""

    def __init__(self, *calendars: MarketCalendar) -> None:
        names = "+".join(c.name for c in calendars)
        weekend: frozenset[int] = frozenset().union(*[c._weekend_days for c in calendars])
        super().__init__(name=names, rules=[], weekend_days=weekend)
        self._calendars = calendars

    def holidays(self, year: int) -> frozenset[date]:
        if year not in self._cache:
            result: set[date] = set()
            for cal in self._calendars:
                result |= cal.holidays(year)
            self._cache[year] = frozenset(result)
        return self._cache[year]


# ---------------------------------------------------------------------------
# G10 Holiday Rule Sets
# ---------------------------------------------------------------------------

def _usd_rules(year: int) -> set[date]:
    """Federal Reserve / NYSE holidays."""
    e = _easter(year)
    rules: set[date] = {
        _observed(date(year, 1, 1)),                         # New Year's Day
        _nth_weekday(year, 1, 0, 3),                         # MLK Day (3rd Mon Jan)
        _nth_weekday(year, 2, 0, 3),                         # Presidents' Day (3rd Mon Feb)
        e - timedelta(days=2),                               # Good Friday
        _last_weekday(year, 5, 0),                           # Memorial Day (last Mon May)
        _observed(date(year, 6, 19)),                        # Juneteenth
        _observed(date(year, 7, 4)),                         # Independence Day
        _nth_weekday(year, 9, 0, 1),                         # Labor Day (1st Mon Sep)
        _nth_weekday(year, 11, 3, 4),                        # Thanksgiving (4th Thu Nov)
        _nth_weekday(year, 11, 3, 4) + timedelta(days=1),   # Day after Thanksgiving
        _observed(date(year, 12, 25)),                       # Christmas
    }
    return rules


def _eur_rules(year: int) -> set[date]:
    """ECB TARGET2 holidays."""
    e = _easter(year)
    return {
        date(year, 1, 1),           # New Year's Day
        e - timedelta(days=2),      # Good Friday
        e + timedelta(days=1),      # Easter Monday
        date(year, 5, 1),           # Labour Day
        date(year, 12, 25),         # Christmas
        date(year, 12, 26),         # Boxing Day / St Stephen's
    }


def _gbp_rules(year: int) -> set[date]:
    """Bank of England holidays."""
    e = _easter(year)
    rules: set[date] = {
        _observed(date(year, 1, 1)),   # New Year's Day
        e - timedelta(days=2),         # Good Friday
        e + timedelta(days=1),         # Easter Monday
        _nth_weekday(year, 5, 0, 1),   # Early May Bank Holiday (1st Mon May)
        _last_weekday(year, 5, 0),     # Spring Bank Holiday (last Mon May)
        _last_weekday(year, 8, 0),     # Summer Bank Holiday (last Mon Aug)
        _observed(date(year, 12, 25)), # Christmas
        _observed(date(year, 12, 26)), # Boxing Day
    }
    return rules


def _jpy_rules(year: int) -> set[date]:
    """Bank of Japan / Tokyo Stock Exchange holidays (major recurring)."""
    e = _easter(year)  # not used for JPY but keeping import consistent
    _ = e  # suppress unused warning
    rules: set[date] = {
        date(year, 1, 1),                       # New Year's Day (Ganjitsu)
        date(year, 1, 2),                       # Bank Holiday
        date(year, 1, 3),                       # Bank Holiday
        _nth_weekday(year, 1, 0, 2),            # Coming of Age Day (2nd Mon Jan)
        _observed(date(year, 2, 11)),            # National Foundation Day
        _observed(date(year, 2, 23)),            # Emperor's Birthday
        _observed(date(year, 3, 20)),            # Vernal Equinox (approx)
        _observed(date(year, 4, 29)),            # Showa Day
        _observed(date(year, 5, 3)),             # Constitution Memorial Day
        _observed(date(year, 5, 4)),             # Greenery Day
        _observed(date(year, 5, 5)),             # Children's Day
        _nth_weekday(year, 7, 0, 3),            # Marine Day (3rd Mon Jul)
        _nth_weekday(year, 8, 0, 3),            # Mountain Day — 3rd Mon Aug approx
        _observed(date(year, 8, 11)),            # Mountain Day (fixed)
        _nth_weekday(year, 9, 0, 3),            # Respect for the Aged (3rd Mon Sep)
        _observed(date(year, 9, 23)),            # Autumnal Equinox (approx)
        _nth_weekday(year, 10, 0, 2),           # Sports Day (2nd Mon Oct)
        _observed(date(year, 11, 3)),            # Culture Day
        _observed(date(year, 11, 23)),           # Labour Thanksgiving Day
        date(year, 12, 31),                     # New Year's Eve (bank holiday)
    }
    return rules


def _chf_rules(year: int) -> set[date]:
    """Swiss National Bank / SIX holidays."""
    e = _easter(year)
    return {
        date(year, 1, 1),               # New Year's Day
        date(year, 1, 2),               # Berchtoldstag
        e - timedelta(days=2),          # Good Friday
        e + timedelta(days=1),          # Easter Monday
        date(year, 5, 1),               # Labour Day
        e + timedelta(days=39),         # Ascension Day
        e + timedelta(days=50),         # Whit Monday
        date(year, 8, 1),               # National Day
        date(year, 12, 25),             # Christmas
        date(year, 12, 26),             # St Stephen's Day
    }


def _cad_rules(year: int) -> set[date]:
    """Bank of Canada holidays."""
    e = _easter(year)
    rules: set[date] = {
        _observed(date(year, 1, 1)),        # New Year's Day
        e - timedelta(days=2),              # Good Friday
        e + timedelta(days=1),              # Easter Monday
        _nth_weekday(year, 5, 0, 3)        # Victoria Day — Mon before May 25
        if _nth_weekday(year, 5, 0, 3) < date(year, 5, 25)
        else _nth_weekday(year, 5, 0, 2),
        _observed(date(year, 7, 1)),        # Canada Day
        _nth_weekday(year, 8, 0, 1),        # Civic Holiday (1st Mon Aug)
        _nth_weekday(year, 9, 0, 1),        # Labour Day (1st Mon Sep)
        _nth_weekday(year, 10, 0, 2),       # Thanksgiving (2nd Mon Oct)
        _observed(date(year, 11, 11)),       # Remembrance Day
        _observed(date(year, 12, 25)),       # Christmas
        _observed(date(year, 12, 26)),       # Boxing Day
    }
    return rules


def _aud_rules(year: int) -> set[date]:
    """Reserve Bank of Australia / ASX holidays."""
    e = _easter(year)
    rules: set[date] = {
        _observed(date(year, 1, 1)),        # New Year's Day
        _observed(date(year, 1, 26)),       # Australia Day
        e - timedelta(days=2),              # Good Friday
        e - timedelta(days=1),              # Easter Saturday
        e + timedelta(days=1),              # Easter Monday
        _observed(date(year, 4, 25)),       # ANZAC Day
        _nth_weekday(year, 6, 0, 2),        # Queen's Birthday (2nd Mon Jun)
        _nth_weekday(year, 8, 0, 1),        # Bank Holiday (1st Mon Aug)
        _nth_weekday(year, 10, 0, 1),       # Labour Day (1st Mon Oct)
        _observed(date(year, 12, 25)),      # Christmas
        _observed(date(year, 12, 26)),      # Boxing Day
    }
    return rules


def _nzd_rules(year: int) -> set[date]:
    """Reserve Bank of New Zealand / NZX holidays."""
    e = _easter(year)
    rules: set[date] = {
        _observed(date(year, 1, 1)),        # New Year's Day
        _observed(date(year, 1, 2)),        # Day after New Year's
        _observed(date(year, 2, 6)),        # Waitangi Day
        e - timedelta(days=2),              # Good Friday
        e + timedelta(days=1),              # Easter Monday
        _observed(date(year, 4, 25)),       # ANZAC Day
        _nth_weekday(year, 6, 0, 1),        # Queen's Birthday (1st Mon Jun)
        _nth_weekday(year, 10, 0, 4),       # Labour Day (4th Mon Oct)
        _observed(date(year, 12, 25)),      # Christmas
        _observed(date(year, 12, 26)),      # Boxing Day
    }
    return rules


def _sek_rules(year: int) -> set[date]:
    """Riksbank / Nasdaq Stockholm holidays."""
    e = _easter(year)
    return {
        date(year, 1, 1),               # New Year's Day
        date(year, 1, 6),               # Epiphany
        e - timedelta(days=2),          # Good Friday
        e + timedelta(days=1),          # Easter Monday
        date(year, 5, 1),               # Labour Day
        e + timedelta(days=39),         # Ascension Day
        date(year, 6, 6),               # National Day
        _nth_weekday(year, 6, 4, 3),    # Midsummer Eve (Fri between Jun 19-25)
        _nth_weekday(year, 12, 4, 1),   # Christmas Eve (nearest Fri)
        date(year, 12, 25),             # Christmas Day
        date(year, 12, 26),             # Boxing Day
        date(year, 12, 31),             # New Year's Eve
    }


def _nok_rules(year: int) -> set[date]:
    """Norges Bank holidays."""
    e = _easter(year)
    return {
        date(year, 1, 1),               # New Year's Day
        e - timedelta(days=3),          # Maundy Thursday
        e - timedelta(days=2),          # Good Friday
        e + timedelta(days=1),          # Easter Monday
        date(year, 5, 1),               # Labour Day
        date(year, 5, 17),              # Constitution Day
        e + timedelta(days=39),         # Ascension Day
        e + timedelta(days=49),         # Whit Sunday
        e + timedelta(days=50),         # Whit Monday
        date(year, 12, 25),             # Christmas
        date(year, 12, 26),             # Boxing Day
    }


def _dkk_rules(year: int) -> set[date]:
    """Danmarks Nationalbank holidays."""
    e = _easter(year)
    return {
        date(year, 1, 1),               # New Year's Day
        e - timedelta(days=3),          # Maundy Thursday
        e - timedelta(days=2),          # Good Friday
        e + timedelta(days=1),          # Easter Monday
        e + timedelta(days=26),         # General Prayer Day (Store Bededag) — abolished 2024
        date(year, 5, 1),               # Labour Day (banks only)
        e + timedelta(days=39),         # Ascension Day
        e + timedelta(days=50),         # Whit Monday
        date(year, 6, 5),               # Constitution Day
        _observed(date(year, 12, 24)),  # Christmas Eve
        date(year, 12, 25),             # Christmas
        date(year, 12, 26),             # Boxing Day
        date(year, 12, 31),             # New Year's Eve
    }


# ---------------------------------------------------------------------------
# Calendar registry
# ---------------------------------------------------------------------------

_CALENDARS: dict[str, MarketCalendar] = {
    "USD": MarketCalendar("USD/FED", [_usd_rules]),
    "EUR": MarketCalendar("EUR/ECB", [_eur_rules]),
    "GBP": MarketCalendar("GBP/BOE", [_gbp_rules]),
    "JPY": MarketCalendar("JPY/BOJ", [_jpy_rules]),
    "CHF": MarketCalendar("CHF/SNB", [_chf_rules]),
    "CAD": MarketCalendar("CAD/BOC", [_cad_rules]),
    "AUD": MarketCalendar("AUD/RBA", [_aud_rules]),
    "NZD": MarketCalendar("NZD/RBNZ", [_nzd_rules]),
    "SEK": MarketCalendar("SEK/RIX", [_sek_rules]),
    "NOK": MarketCalendar("NOK/NB", [_nok_rules]),
    "DKK": MarketCalendar("DKK/DNB", [_dkk_rules]),
}


def get_calendar(currency: Currency | str) -> MarketCalendar:
    """Return the MarketCalendar for the given currency code."""
    key = str(currency).upper()
    try:
        return _CALENDARS[key]
    except KeyError:
        raise ValueError(f"No market calendar for currency {key!r}") from None


# ---------------------------------------------------------------------------
# Module-level convenience functions
# ---------------------------------------------------------------------------

def is_business_day(d: date, cal: MarketCalendar) -> bool:
    return cal.is_business_day(d)


def next_business_day(d: date, cal: MarketCalendar) -> date:
    return cal.next_business_day(d)


def add_business_days(d: date, n: int, cal: MarketCalendar) -> date:
    return cal.add_business_days(d, n)
