---
id: db-repository-layer
title: Repository layer async (CRUD)
intent: database-swagger
complexity: medium
mode: confirm
status: pending
depends_on: [db-alembic-migrations]
created: 2026-05-25T12:00:00Z
---

# Work Item: Repository Layer

## Description

Créer les repositories async pour lire/écrire les entités FX depuis PostgreSQL. Chaque repository encapsule les requêtes SQLAlchemy et retourne des objets du domaine (pas des modèles ORM).

## Acceptance Criteria

- [ ] `app/infrastructure/repositories/convention_repository.py` — `get_all()`, `get_by_pair()`
- [ ] `app/infrastructure/repositories/calendar_repository.py` — `get_by_currency()`, `get_holidays(currency, year)`
- [ ] Les repositories retournent des types du domaine (`FxConvention`, `MarketCalendar`)
- [ ] Tests unitaires avec une DB SQLite in-memory ou des mocks SQLAlchemy

## Technical Notes

- Pattern Repository : les repositories reçoivent `AsyncSession` en paramètre (injection)
- Mapper ORM → domaine dans le repository (pas dans l'API layer)
- Utiliser `select()` SQLAlchemy 2.0 style (pas l'ancien `session.query()`)

## Dependencies

- db-alembic-migrations
