---
id: frontend-scaffold
title: Frontend Scaffold (Vite + React + TypeScript + Tailwind)
intent: frontend-fx-reference
complexity: low
mode: autopilot
status: pending
depends_on: [project-scaffold]
created: "2026-05-22T00:00:00Z"
---

# Work Item: Frontend Scaffold

## Description

Initialiser le projet frontend dans `frontend/` : Vite 5 + React 18 + TypeScript strict + Tailwind CSS 3. Configuration ESLint 9 (flat config) + Prettier. Structure de dossiers : `components/`, `features/`, `hooks/`, `types/`, `services/` (client API). Dev server sur port 3000.

Fichiers cibles :
- `frontend/` — projet complet
- `frontend/src/services/api.ts` — client HTTP de base (fetch + base URL)
- `frontend/src/types/fx.ts` — types TypeScript domaine FX (FXConvention, Calendar, etc.)

## Acceptance Criteria

- [ ] `pnpm dev` démarre le dev server sur http://localhost:3000 sans erreur
- [ ] `pnpm build` produit un build sans erreur TypeScript
- [ ] `pnpm lint` passe sans warning (ESLint + Prettier)
- [ ] `pnpm test` passe (Vitest, 0 tests collectés)
- [ ] Tailwind CSS configuré et fonctionnel (classe `bg-blue-500` visible dans App.tsx)
- [ ] `frontend/src/types/fx.ts` définit : `FXConvention`, `Currency`, `CurrencyPair`, `CalendarHoliday`, `SpotDateResult`
- [ ] `frontend/src/services/api.ts` exporte `fetchConventions()`, `fetchConvention(pair)`, `fetchHolidays(currency, year)`, `checkBusinessDay(currency, date)`, `calculateSpotDate(pair, tradeDate, tenor)`
- [ ] Service ajouté dans `docker-compose.yml` (port 3000, volume `./frontend:/app`, `pnpm dev`)

## Technical Notes

- pnpm comme package manager
- TypeScript `strict: true` dans tsconfig
- `VITE_API_BASE_URL=http://localhost:8000` dans `.env.local`
- Path alias `@/` → `src/`

## Dependencies

- project-scaffold
