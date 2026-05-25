---
id: database-swagger
title: Base de données & Swagger UI
status: in_progress
created: 2026-05-25T12:00:00Z
---

# Intent: Base de données & Swagger UI

## Goal

Connecter le backend FastAPI à PostgreSQL via SQLAlchemy async + Alembic, et exposer une page Swagger UI propre et navigable.

## Users

Développeurs qui intègrent l'API et traders qui consultent la documentation pour comprendre les endpoints disponibles.

## Problem

Le backend tourne mais sans persistance — les données FX (conventions, calendriers, holidays) sont statiques en mémoire. Il n'y a pas de vraie base de données, pas de migrations versionnées, et le Swagger est générique sans organisation ni exemples.

## Success Criteria

- `alembic upgrade head` crée les tables FX (conventions, calendriers, holidays) sans erreur
- Les endpoints conventions et calendriers lisent depuis PostgreSQL via SQLAlchemy async
- La page Swagger UI (`/docs`) est organisée par tags, avec descriptions et exemples de réponse
- Le schéma OpenAPI reflète fidèlement les types FX du domaine existant
- Pas de breaking change sur les endpoints existants

## Constraints

- Stack imposée : SQLAlchemy 2.0 async + Alembic + PostgreSQL 16
- Le domaine FX existe déjà dans `app/domain/` — les modèles DB mappent dessus
- Les endpoints REST existants (`/conventions`, `/calendars`) doivent continuer à fonctionner

## Notes

(none)
