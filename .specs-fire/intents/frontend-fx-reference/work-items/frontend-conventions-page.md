---
id: frontend-conventions-page
title: Page Conventions FX
intent: frontend-fx-reference
complexity: medium
mode: confirm
status: completed
depends_on:
  - frontend-scaffold
  - api-fx-reference-data
created: 2026-05-22T00:00:00Z
run_id: run-fx-pricing-012
completed_at: 2026-05-23T11:42:25.283Z
---

# Work Item: Page Conventions FX

## Description

Page React `/conventions` : liste et recherche des conventions FX. Searchbox pour filtrer par paire, tableau détaillé de la convention sélectionnée (spot lag, day count basis, pip precision, roll convention, quotation side). Toutes les paires G10 affichées par défaut.

Fichiers cibles :
- `frontend/src/features/conventions/ConventionsPage.tsx`
- `frontend/src/features/conventions/ConventionDetail.tsx`
- `frontend/src/features/conventions/ConventionsList.tsx`
- `frontend/src/hooks/useConventions.ts`

## Acceptance Criteria

- [ ] Route `/conventions` affiche la liste de toutes les paires G10 disponibles
- [ ] Searchbox filtre les paires en temps réel (ex: taper "EUR" → montre EURUSD, EURGBP, EURJPY, EURCHF)
- [ ] Cliquer sur une paire affiche le détail complet de sa convention
- [ ] Détail affiche : Spot Lag, Day Count Basis, Roll Convention, Pip Precision, Quotation Side
- [ ] État de chargement (skeleton/spinner) pendant le fetch API
- [ ] Message d'erreur si l'API est inaccessible
- [ ] Paire invalide dans l'URL → message "Convention non trouvée"
- [ ] Responsive : lisible sur desktop et tablet

## Technical Notes

- `useConventions()` hook custom — fetch via `services/api.ts`
- Pas de librairie de state global (Zustand) pour cet écran — état local suffisant
- Navigation via React Router v6

## Dependencies

- frontend-scaffold
- api-fx-reference-data
