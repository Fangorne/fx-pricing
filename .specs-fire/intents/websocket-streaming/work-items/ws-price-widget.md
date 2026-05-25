---
id: ws-price-widget
title: SpotPriceTicker Component
intent: websocket-streaming
complexity: medium
mode: confirm
status: pending
depends_on: [ws-frontend-hook]
created: 2026-05-25T17:45:00Z
---

# Work Item: SpotPriceTicker Component

## Description

Composant React `<SpotPriceTicker />` qui affiche le prix spot live d'une paire FX. Utilise `useSpotStream`. Affiche bid / ask / mid avec une animation flash à chaque mise à jour de prix. Inclut un badge de statut de connexion et un dropdown pour sélectionner la paire.

## Acceptance Criteria

- [ ] `frontend/src/components/trading/SpotPriceTicker.tsx` — composant principal
- [ ] Affiche : paire, bid, ask, mid (formatés selon pip precision), timestamp
- [ ] Flash animation sur chaque update de prix (CSS keyframe `priceFlash` — vert si mid monte, rouge si descend)
- [ ] Badge statut : `LIVE` (vert), `RECONNECTING` (jaune), `ERROR` (rouge), `CLOSED` (gris)
- [ ] Dropdown pour sélectionner la paire parmi toutes les paires G10
- [ ] Prop `defaultPair?: string` (défaut `"EUR/USD"`)
- [ ] État `is_stale` affiché avec un indicateur visuel (horloge ou texte "Stale")
- [ ] Skeleton loading pendant la connexion initiale

## Technical Notes

- Utiliser `useRef` pour tracker le `prevMid` et déterminer la direction du flash
- Flash : `animate-[priceFlash_400ms_ease-out]` via Tailwind arbitrary + `@keyframes priceFlash` dans `index.css`
- Couleurs : utiliser les tokens CSS `var(--positive)` / `var(--negative)` du design system
- Format nombres : `toFixed(pair pip precision)` — récupérer depuis les conventions existantes ou hardcoder par paire
- Dropdown : réutiliser les styles existants du design system

## Dependencies

- ws-frontend-hook
