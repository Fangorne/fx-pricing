---
id: frontend-calendar-page
title: Page Calendrier de Marché
intent: frontend-fx-reference
complexity: medium
mode: confirm
status: pending
depends_on: [frontend-scaffold, api-fx-reference-data]
created: "2026-05-22T00:00:00Z"
---

# Work Item: Page Calendrier de Marché

## Description

Page React `/calendars` : exploration des calendriers de marché par devise. Sélecteur de devise, vue liste des jours fériés pour une année donnée, et vérificateur de date (is_business_day). Résultat coloré : vert = business day, rouge = non business day avec raison.

Fichiers cibles :
- `frontend/src/features/calendars/CalendarPage.tsx`
- `frontend/src/features/calendars/HolidayList.tsx`
- `frontend/src/features/calendars/BusinessDayChecker.tsx`
- `frontend/src/hooks/useCalendar.ts`

## Acceptance Criteria

- [ ] Route `/calendars` avec sélecteur de devise (USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD, SEK, NOK)
- [ ] Sélection devise → affiche la liste des jours fériés pour l'année en cours
- [ ] Sélecteur d'année (année courante ± 2 ans) pour changer l'année affichée
- [ ] Chaque jour férié affiché avec : date formatée, nom du jour férié
- [ ] Section "Vérifier une date" : input date → appel API → badge vert "Business Day" ou rouge "Non ouvré — [raison]"
- [ ] Résultat is_business_day mis à jour immédiatement à la saisie de la date (debounce 300ms)
- [ ] Weekend détecté et affiché comme "Weekend" (sans appel API inutile)
- [ ] État de chargement pendant le fetch

## Technical Notes

- `useCalendar(currency, year)` hook — refetch automatique si currency ou year change
- Debounce 300ms sur le vérificateur de date
- Weekends détectés côté client (samedi/dimanche) avant appel API

## Dependencies

- frontend-scaffold
- api-fx-reference-data
