---
id: docker-ci-setup
title: Dockerisation & CI GitHub
status: in_progress
created: "2026-05-22T00:00:00Z"
---

# Intent: Dockerisation & CI GitHub

## Goal

Mettre en place la containerisation Docker et les pipelines CI GitHub Actions — infrastructure de développement et de qualité reproductible pour tout le projet.

## Users

Tous les développeurs du projet (setup local immédiat, feedback CI automatique sur chaque PR).

## Problem

Sans Docker et CI, l'environnement de dev n'est pas reproductible et la qualité du code n'est pas vérifiée automatiquement. C'est un prérequis pour que les autres intents (backend, market data, pricing) soient livrables.

## Success Criteria

- `docker compose up` démarre l'environnement complet (backend, postgres, redis) en une commande
- Le service backend monte le code en live-reload en mode dev
- GitHub Actions déclenche lint (Ruff + mypy) + tests (pytest) sur chaque push/PR vers main
- Le CI passe au vert sur un projet Python vide (base pour les futurs runs)
- Dockerfile backend multi-stage (dev + prod)

## Constraints

- Python 3.12 / uv (pas pip/poetry)
- GitHub Actions uniquement
- Docker Compose v2

## Notes

Dépend de `project-scaffold` (intent core-fx-domain) pour la structure du projet Python.
