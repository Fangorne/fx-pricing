---
id: dockerfile-backend
title: Dockerfile Backend Multi-Stage
intent: docker-ci-setup
complexity: low
mode: autopilot
status: pending
depends_on: [project-scaffold]
created: "2026-05-22T00:00:00Z"
---

# Work Item: Dockerfile Backend Multi-Stage

## Description

Créer le `Dockerfile` multi-stage pour le backend Python/uv : stage `dev` (uv, uvicorn avec hot-reload) et stage `prod` (image allégée, gunicorn + uvicorn workers). Ajouter `.dockerignore` adapté.

Fichiers cibles :
- `backend/Dockerfile`
- `backend/.dockerignore`

## Acceptance Criteria

- [ ] Stage `dev` : base `python:3.12-slim`, installe uv, copie pyproject.toml, installe deps, monte le code via volume (pas COPY), lance `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- [ ] Stage `prod` : image minimale, `uv sync --no-dev`, lance gunicorn avec workers uvicorn
- [ ] `.dockerignore` exclut : `__pycache__`, `.venv`, `*.pyc`, `.mypy_cache`, `.ruff_cache`, `tests/`
- [ ] `docker build --target dev -t fx-pricing-backend:dev .` réussit sans erreur
- [ ] `docker build --target prod -t fx-pricing-backend:prod .` réussit sans erreur
- [ ] Image prod < 300MB

## Technical Notes

- Utiliser `uv sync --frozen` pour la reproductibilité
- Layer ordering optimisé : copier pyproject.toml + uv.lock avant le code source (cache Docker)
- Port exposé : 8000

## Dependencies

- project-scaffold
