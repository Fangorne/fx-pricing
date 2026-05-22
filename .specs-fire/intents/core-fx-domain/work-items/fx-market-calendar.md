---
id: fx-market-calendar
title: FX Market Calendar
intent: core-fx-domain
complexity: medium
mode: confirm
status: pending
depends_on: [fx-core-types]
created: "2026-05-22T00:00:00Z"
---

# Work Item: FX Market Calendar

## Description

Implémenter `MarketCalendar` : jours fériés par devise (USD/FED, EUR/ECB TARGET, GBP/BOE, JPY/BOJ, CHF/SNB, CAD, AUD, NZD, SEK, NOK, DKK), weekends configurables (Sat+Sun par défaut), `is_business_day(date) → bool`, `next_business_day(date) → date`, `add_business_days(date, n) → date`. Calendriers combinés multi-devises via union des jours fériés.

Fichiers cibles :
- `app/domain/calendar.py` — `MarketCalendar`, `CombinedCalendar`, `get_calendar(currency)`
- `tests/unit/domain/test_calendar.py`

## Acceptance Criteria

- [ ] `get_calendar("USD").is_business_day(date(2026, 1, 1))` → False (New Year)
- [ ] `get_calendar("USD").is_business_day(date(2026, 7, 4))` → False (Independence Day)
- [ ] `get_calendar("USD").is_business_day(date(2026, 11, 26))` → False (Thanksgiving)
- [ ] `get_calendar("EUR").is_business_day(date(2026, 12, 25))` → False (Christmas)
- [ ] `get_calendar("EUR").is_business_day(date(2026, 4, 3))` → False (Good Friday 2026)
- [ ] `get_calendar("JPY").is_business_day(date(2026, 1, 1))` → False
- [ ] Samedi/Dimanche → False pour toutes les devises
- [ ] `CombinedCalendar(usd, eur).is_business_day(d)` → False si férié dans l'un ou l'autre
- [ ] `add_business_days(date(2026, 5, 22), 2, usd_calendar)` → date(2026, 5, 26) (skip WE)
- [ ] Tests couvrent tous les G10 avec au moins 3 jours fériés vérifiés par devise

## Technical Notes

- Jours fériés définis statiquement par règle (ex: "premier lundi de septembre" pour Labor Day US) plutôt que liste exhaustive année par année
- Utiliser `datetime.date` (pas `datetime.datetime`)
- `get_calendar(currency: Currency | str) → MarketCalendar` comme factory function

## Dependencies

- fx-core-types
