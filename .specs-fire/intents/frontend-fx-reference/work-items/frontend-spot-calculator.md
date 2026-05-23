---
id: frontend-spot-calculator
title: Calculateur de Dates Spot/Value
intent: frontend-fx-reference
complexity: medium
mode: confirm
status: completed
depends_on:
  - frontend-conventions-page
  - frontend-calendar-page
created: 2026-05-22T00:00:00Z
run_id: run-fx-pricing-014
completed_at: 2026-05-23T11:58:29.215Z
---

# Work Item: Calculateur de Dates Spot/Value

## Description

Page React `/dates` : calculateur interactif de dates spot et value. Sélecteur paire FX + date de trade + ténor → affichage immédiat de la date spot et de la date value calculées via l'API backend. Affiche aussi le nombre de business days entre trade date et spot date.

Fichiers cibles :
- `frontend/src/features/dates/SpotCalculatorPage.tsx`
- `frontend/src/features/dates/DateResult.tsx`
- `frontend/src/hooks/useSpotDate.ts`

## Acceptance Criteria

- [ ] Route `/dates` avec formulaire : sélecteur paire (dropdown G10), date picker trade date, sélecteur ténor (ON, TN, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y)
- [ ] À chaque changement de champ → appel API automatique (debounce 300ms)
- [ ] Résultat affiché : Spot Date (formaté DD MMM YYYY), Value Date (formaté DD MMM YYYY)
- [ ] Indication si la spot date ou value date tombe un weekend/férié et comment elle a été ajustée
- [ ] Affichage de la convention utilisée pour le calcul (spot lag, roll convention)
- [ ] Erreur de saisie (date invalide, paire non supportée) → message clair inline
- [ ] Historique des 5 derniers calculs affiché sous le formulaire (état local)

## Technical Notes

- `useSpotDate(pair, tradeDate, tenor)` hook — skip si champs incomplets
- Debounce 300ms — pas d'appel API à chaque keystroke
- Date picker natif HTML (`<input type="date">`) — pas de librairie externe

## Dependencies

- frontend-conventions-page
- frontend-calendar-page
