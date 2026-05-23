---
run: run-fx-pricing-003
work_item: fx-market-calendar
intent: core-fx-domain
mode: confirm
checkpoint: approved
generated: "2026-05-23T10:16:30Z"
---

# Plan: FX Market Calendar

## Approach

Holiday rules defined algorithmically (rule-based) using stdlib only. Each currency gets a `MarketCalendar` built from `HolidayRule` callables. `CombinedCalendar` takes the union. Easter computed via Meeus/Jones/Butcher algorithm. Holidays cached per year inside each calendar instance.

## Files to Create

| File | Purpose |
|------|---------|
| `backend/app/domain/calendar.py` | `MarketCalendar`, `CombinedCalendar`, `get_calendar()`, helpers |
| `backend/tests/unit/domain/test_calendar.py` | G10 coverage, ≥3 holidays each, combined/add_business_days |

## Files to Modify

None.

## Key Decisions

| Decision | Choice |
|----------|--------|
| Holiday computation | Rule-based callables, cached per year |
| Easter | Meeus/Jones/Butcher (stdlib only) |
| Observed rules | Sat → Fri, Sun → Mon |
| Weekend | Saturday + Sunday (configurable) |
