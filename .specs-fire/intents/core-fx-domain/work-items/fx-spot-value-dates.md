---
id: fx-spot-value-dates
title: FX Spot and Value Date Generation
intent: core-fx-domain
complexity: medium
mode: confirm
status: pending
depends_on: [fx-business-day-rules]
created: "2026-05-22T00:00:00Z"
---

# Work Item: FX Spot and Value Date Generation

## Description

Implémenter `spot_date(trade_date, pair, calendar) → date` et `value_date(trade_date, tenor, pair, calendar, convention) → date`. Gestion du spot lag par paire (T+1 pour USD/CAD et USD/TRY, T+2 pour la plupart des G10, T+0 pour certains cas). Cas spéciaux ON (overnight = T+1), TN (tom-next = T+2), SN (spot-next = spot+1).

Fichiers cibles :
- `app/domain/date_generation.py` — `spot_date()`, `value_date()`, `SPOT_LAGS`
- `tests/unit/domain/test_date_generation.py`

## Acceptance Criteria

- [ ] `spot_date(date(2026,5,22), EURUSD, eur_usd_calendar)` → date(2026,5,26) (vendredi → skip WE → mardi)
- [ ] `spot_date(date(2026,5,22), USDCAD, usd_cad_calendar)` → T+1 = date(2026,5,25) (lundi)
- [ ] Ténor ON : `value_date(trade_date, ON, ...)` → trade_date + 1 BD
- [ ] Ténor TN : `value_date(trade_date, TN, ...)` → spot_date - 1 BD (= trade_date + 1 BD)
- [ ] Ténor 3M EUR/USD : `value_date(date(2026,5,22), 3M, ...)` → date(2026,8,26) ajusté ModifiedFollowing
- [ ] Ténor 1Y EUR/USD depuis fin de mois : EOM rule respectée si applicable
- [ ] Tests avec dates incluant jours fériés USD et EUR
- [ ] Toutes les paires G10 testées pour spot_date (au moins 3 trade_dates par paire)

## Technical Notes

- Spot lag par défaut T+2, exceptions : USD/CAD=T+1, USD/TRY=T+1, USD/RUB=T+1
- Le calendrier pour spot_date est un `CombinedCalendar` des deux devises de la paire + USD (USD est toujours inclus sauf USD/CAD)
- Les mois sont ajoutés en suivant la convention EOM/ModifiedFollowing selon la convention de la paire

## Dependencies

- fx-business-day-rules
