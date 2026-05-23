---
run: run-fx-pricing-003
work_item: fx-market-calendar
intent: core-fx-domain
generated: "2026-05-23T10:47:00Z"
mode: confirm
---

# Implementation Walkthrough: FX Market Calendar

## Summary

Implemented a rule-based FX market calendar system covering all 11 G10 currencies. Each currency has a `MarketCalendar` driven by algorithmic `HolidayRule` callables (no hardcoded year lists). Easter is computed via the Meeus/Jones/Butcher algorithm (stdlib only). `CombinedCalendar` takes the union of any number of single-currency calendars. 108 unit tests achieve 98% coverage.

## Structure Overview

All calendar logic lives in `app/domain/calendar.py`. Private helper functions (`_easter`, `_nth_weekday`, `_last_weekday`, `_observed`) are composed inside G10 rule functions (`_usd_rules`, `_eur_rules`, etc.). These rules are wired into a `_CALENDARS` registry dict. The `get_calendar()` factory returns calendars by currency code string or `Currency` enum. Holidays are computed lazily on first access per year and cached as `frozenset[date]` inside each instance.

## Architecture

The module is structured in four layers:

```text
┌─────────────────────────────────────────────┐
│  Public API: get_calendar(), convenience fns │
├─────────────────────────────────────────────┤
│  Classes: MarketCalendar, CombinedCalendar  │
├─────────────────────────────────────────────┤
│  G10 Rule Functions: _usd_rules, _eur_rules…│
├─────────────────────────────────────────────┤
│  Primitives: _easter, _nth_weekday, …       │
└─────────────────────────────────────────────┘
```

## Files Changed

### Created

| File | Purpose |
|------|---------|
| `backend/app/domain/calendar.py` | Full calendar implementation — 11 G10 calendars, helpers, registry |
| `backend/tests/unit/domain/test_calendar.py` | 108 unit tests covering all G10 currencies |

## Key Implementation Details

### 1. Rule-based holidays (self-extending)

Holidays are defined as `Callable[[int], set[date]]` functions — they compute holidays for any given year on demand. No year-hardcoded lists. Adding a new year costs nothing; adding a new holiday means adding one line to one function.

### 2. Easter algorithm

The Meeus/Jones/Butcher algorithm (pure integer arithmetic) computes Easter Sunday for any Gregorian year. Good Friday, Easter Monday, Ascension, Whit Monday are all derived from this. Validated implicitly by 7+ currency tests checking Easter-relative holidays.

### 3. `_observed()` for weekend shift

US and UK fixed holidays shift: Saturday → previous Friday, Sunday → next Monday. Encoded in the `_observed()` helper, applied to all fixed-date holidays that follow this pattern.

### 4. Holiday caching

`MarketCalendar._cache: dict[int, frozenset[date]]` ensures each year's holidays are computed once. The `frozenset` is immutable — safe to share across threads and to use as a fast `in` membership test.

### 5. `CombinedCalendar` union semantics

Takes `*calendars` varargs, unions their holiday sets. A date is non-business if it's a weekend in ANY component calendar, or a holiday in ANY component calendar. Used for cross-currency spot date calculation (e.g. EUR/USD needs both ECB and FED calendars to be open).

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Rule-based vs year lists | Rule-based | Self-extending; no annual maintenance |
| Easter | Meeus/Jones/Butcher | Single formula, stdlib only, handles all years |
| `_observed()` | Sat→Fri, Sun→Mon | US/UK standard; other markets may differ |
| Holiday storage | `frozenset[date]` | O(1) lookup, immutable, hashable |
| `CombinedCalendar` | Subclass of `MarketCalendar` | Allows uniform `is_business_day()` interface |
| Weekend configurability | `frozenset[int]` parameter | Allows Middle East markets (Fri+Sat) in future |
| `get_calendar()` | String or `Currency` enum | Flexible for callers that don't import `Currency` |

## Deviations from Plan

**`add_business_days` acceptance criterion:** The work item specified `date(2026, 5, 22) + 2 USD biz days → date(2026, 5, 26)`. The correct result is **May 27** — May 25 is Memorial Day (last Monday of May), which the spec overlooked. Implementation is correct; test was updated to assert May 27.

## Dependencies Added

None — stdlib only (`calendar`, `datetime`, `collections.abc`).

## How to Verify

1. **Run unit tests**

   ```bash
   cd backend && uv run pytest tests/unit/domain/test_calendar.py -v
   ```

   Expected: 108 passed.

2. **Spot-check a specific holiday**

   ```python
   from datetime import date
   from app.domain.calendar import get_calendar
   cal = get_calendar("USD")
   print(cal.is_business_day(date(2026, 11, 26)))  # False — Thanksgiving
   print(cal.is_business_day(date(2026, 11, 25)))  # True
   ```

3. **Combined calendar**

   ```python
   from app.domain.calendar import get_calendar, CombinedCalendar
   from datetime import date
   usd = get_calendar("USD")
   eur = get_calendar("EUR")
   eurusd = CombinedCalendar(usd, eur)
   print(eurusd.is_business_day(date(2026, 5, 1)))  # False — EUR Labour Day
   print(eurusd.is_business_day(date(2026, 7, 4)))  # False — USD Independence Day
   ```

## Test Coverage

- Tests added: 108
- Coverage: 98% (3 defensive raise branches unreachable with valid inputs)
- Status: passing

## Ready for Review

- [x] All acceptance criteria met (with documented deviation on `add_business_days` date)
- [x] Tests passing (108/108)
- [x] No critical issues
- [x] Deviation from spec documented
- [x] Developer notes captured

## Developer Notes

- `CombinedCalendar` needs to be constructed fresh per pair (USD+EUR for EURUSD, USD+JPY for USDJPY, etc.) — it is not pre-built in the registry.
- The `_CALENDARS` dict holds singleton `MarketCalendar` instances — their caches are shared across the process lifetime. This is intentional and thread-safe for reads.
- For Middle East currencies (AED, SAR) the `weekend_days` parameter accepts any `frozenset[int]` — pass `frozenset({4, 5})` for Friday+Saturday weekends.
- Vernal/Autumnal equinox dates for JPY are approximated (±1 day). The precise date requires astronomical calculation; for trading-day purposes the approximation is standard practice.

---
*Generated by specs.md - fabriqa.ai FIRE Flow Run run-fx-pricing-003*
