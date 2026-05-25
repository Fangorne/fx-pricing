---
id: db-wire-api
title: Wiring API → DB (remplacer données statiques)
intent: database-swagger
complexity: medium
mode: confirm
status: pending
depends_on: [db-repository-layer]
created: 2026-05-25T12:00:00Z
---

# Work Item: Wiring API → DB

## Description

Brancher les endpoints FastAPI existants (`/conventions`, `/calendars`, `/dates`) sur les repositories PostgreSQL à la place des données statiques en mémoire. Injecter la session DB via la dependency `get_db()`.

## Acceptance Criteria

- [ ] `GET /conventions` lit depuis `ConventionRepository` (PostgreSQL)
- [ ] `GET /conventions/{pair}` lit depuis `ConventionRepository`
- [ ] `GET /calendars/{currency}` lit depuis `CalendarRepository`
- [ ] `GET /calendars/{currency}/holidays` accepte le paramètre `year`
- [ ] `POST /dates/spot` continue à fonctionner (logique domaine inchangée)
- [ ] Les réponses JSON sont identiques à avant (pas de breaking change)
- [ ] Erreur 404 propre si paire/currency inconnue

## Technical Notes

- Injecter `AsyncSession` via `Depends(get_db)` dans les routers
- Instancier les repositories dans les endpoints (pas de DI container pour l'instant)
- Conserver les mêmes schémas Pydantic de réponse

## Dependencies

- db-repository-layer
