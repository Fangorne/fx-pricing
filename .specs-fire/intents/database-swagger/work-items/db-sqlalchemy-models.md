---
id: db-sqlalchemy-models
title: SQLAlchemy Models (conventions, calendriers, holidays)
intent: database-swagger
complexity: medium
mode: confirm
status: pending
depends_on: []
created: 2026-05-25T12:00:00Z
---

# Work Item: SQLAlchemy Models

## Description

Créer les modèles SQLAlchemy 2.0 async pour les entités FX : `FxConvention`, `MarketCalendar`, `Holiday`. Ces modèles mappent directement sur les types du domaine existant (`app/domain/types.py`, `app/domain/conventions.py`, `app/domain/calendar.py`).

Créer aussi la session async et le moteur dans `app/infrastructure/database.py`.

## Acceptance Criteria

- [ ] `app/infrastructure/database.py` contient le moteur async et `AsyncSession`
- [ ] `app/infrastructure/models.py` définit `FxConventionModel`, `MarketCalendarModel`, `HolidayModel`
- [ ] Les modèles utilisent `DeclarativeBase` SQLAlchemy 2.0 (style moderne)
- [ ] Les types de colonnes correspondent au domaine FX (CurrencyPair, DayCount, etc.)
- [ ] `get_db()` dependency injectable dans FastAPI

## Technical Notes

- Utiliser `sqlalchemy.ext.asyncio` (AsyncEngine, AsyncSession)
- `DeclarativeBase` de SQLAlchemy 2.0, pas l'ancien `declarative_base()`
- La DATABASE_URL vient de `app/config.py` (`settings.effective_database_url`)
- Mapper `Currency` → `VARCHAR(3)`, `CurrencyPair` → `VARCHAR(7)`, `DayCount` → `VARCHAR(20)`

## Dependencies

(none)
