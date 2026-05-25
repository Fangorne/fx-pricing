---
id: ws-prices-page
title: Live Prices Page & Navigation
intent: websocket-streaming
complexity: low
mode: autopilot
status: pending
depends_on: [ws-price-widget]
created: 2026-05-25T17:45:00Z
---

# Work Item: Live Prices Page & Navigation

## Description

Créer la page `/prices` dans le frontend qui intègre le composant `SpotPriceTicker`. Ajouter l'entrée de navigation "Live Prices" dans la Sidebar. Configurer la route dans le router.

## Acceptance Criteria

- [ ] `frontend/src/features/prices/LivePricesPage.tsx` — page avec `<SpotPriceTicker />`
- [ ] Route `/prices` ajoutée dans `App.tsx` (ou router config)
- [ ] Entrée "Live Prices" dans `Sidebar.tsx` avec icône `TrendingUp` (Lucide)
- [ ] `PageHeader` avec titre "Live Prices" et description
- [ ] `VITE_WS_URL` ajouté dans `frontend/.env.example` (valeur : `ws://localhost:8000`)

## Technical Notes

- Suivre le pattern des pages existantes (CalendarPage, ConventionsPage)
- Icône : `TrendingUp` de lucide-react

## Dependencies

- ws-price-widget
