---
id: docker-compose-dev
title: Docker Compose Dev Environment
intent: docker-ci-setup
complexity: low
mode: autopilot
status: pending
depends_on: [dockerfile-backend]
created: "2026-05-22T00:00:00Z"
---

# Work Item: Docker Compose Dev Environment

## Description

Créer `docker-compose.yml` complet pour l'environnement de développement : service `backend` (build dev, volume code live-reload), `postgres` (16-alpine, volume persistant, healthcheck), `redis` (7-alpine, healthcheck). Variables d'environnement via `.env.example`.

Fichiers cibles :
- `docker-compose.yml` (racine du projet)
- `.env.example`
- `.env` (gitignored)

## Acceptance Criteria

- [ ] `docker compose up` démarre les 3 services sans erreur
- [ ] `backend` : build target `dev`, volume `./backend:/app`, port `8000:8000`, hot-reload actif (modifier un fichier Python recharge uvicorn)
- [ ] `postgres` : image `postgres:16-alpine`, volume nommé persistant, healthcheck `pg_isready`, variables `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` via env
- [ ] `redis` : image `redis:7-alpine`, healthcheck `redis-cli ping`, port `6379:6379`
- [ ] `backend` attend que `postgres` et `redis` soient healthy (`depends_on: condition: service_healthy`)
- [ ] `.env.example` documente toutes les variables requises
- [ ] `docker compose down -v` nettoie proprement
- [ ] `docker compose logs backend` affiche les logs uvicorn

## Technical Notes

- Réseau interne nommé `fx-network`
- Variables backend : `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `DEBUG=true`
- `.env` ajouté au `.gitignore`

## Dependencies

- dockerfile-backend
