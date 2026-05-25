---
id: db-alembic-migrations
title: Migrations Alembic initiales
intent: database-swagger
complexity: medium
mode: confirm
status: pending
depends_on: [db-sqlalchemy-models]
created: 2026-05-25T12:00:00Z
---

# Work Item: Migrations Alembic

## Description

Initialiser Alembic et créer la migration initiale qui génère les tables FX. Ajouter un script de seed pour peupler les données de référence (45 paires G10, 10 calendriers de marché) au premier démarrage.

## Acceptance Criteria

- [ ] `alembic init` configuré dans `backend/alembic/`
- [ ] `alembic.ini` pointe sur `settings.effective_database_url`
- [ ] Migration `0001_initial_fx_tables.py` créée et réversible (`upgrade` + `downgrade`)
- [ ] `alembic upgrade head` crée les tables sans erreur sur PostgreSQL 16
- [ ] Script `backend/scripts/seed.py` insère les conventions G10 et calendriers de marché

## Technical Notes

- `env.py` Alembic doit importer les models pour l'autogenerate
- Utiliser `--autogenerate` depuis les modèles SQLAlchemy
- La DATABASE_URL sync (psycopg2) pour Alembic, async (asyncpg) pour l'app — deux URLs
- Seed data : reprendre les données statiques existantes dans `app/domain/conventions.py`

## Dependencies

- db-sqlalchemy-models
