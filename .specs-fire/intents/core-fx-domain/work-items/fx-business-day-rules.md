---
id: fx-business-day-rules
title: Business Day Adjustment Rules
intent: core-fx-domain
complexity: medium
mode: confirm
status: completed
depends_on:
  - fx-market-calendar
created: 2026-05-22T00:00:00Z
run_id: run-fx-pricing-004
completed_at: 2026-05-23T10:26:26.943Z
---

# Work Item: Business Day Adjustment Rules

## Description

Implémenter `BusinessDayConvention` enum et la fonction `adjust(date, convention, calendar) → date`. Conventions : Following, ModifiedFollowing, Preceding, ModifiedPreceding, EndOfMonth (EOM).

Fichiers cibles :
- `app/domain/business_day.py` — `BusinessDayConvention`, `adjust()`
- `tests/unit/domain/test_business_day.py`

## Acceptance Criteria

- [ ] `Following` : si férié/WE → avance au prochain business day (peut changer de mois)
- [ ] `ModifiedFollowing` : avance sauf si ça change de mois → recule alors au dernier BD du mois
- [ ] `Preceding` : si férié/WE → recule au BD précédent (peut changer de mois)
- [ ] `ModifiedPreceding` : recule sauf si ça change de mois → avance alors au premier BD du mois
- [ ] `EndOfMonth` : si date source est dernier BD du mois, date ajustée est aussi dernier BD du mois cible
- [ ] Test vendredi → Following = lundi suivant
- [ ] Test samedi → Following = lundi suivant (ou mardi si lundi férié)
- [ ] Test 31 mars (dimanche) → ModifiedFollowing = 30 mars (reste en mars)
- [ ] Test 30 avril (vendredi) → Following = 2 mai (lundi), ModifiedFollowing = 30 avril (reste en avril, c'est déjà BD)
- [ ] Tests exhaustifs avec calendrier USD pour chaque convention

## Technical Notes

- `BusinessDayConvention` : `enum.Enum` avec valeurs string lisibles ("FOLLOWING", etc.)
- `adjust()` est une fonction pure — pas de side effects
- Compatible avec n'importe quel `MarketCalendar`

## Dependencies

- fx-market-calendar
