---
id: project-scaffold
title: Project Scaffold
intent: core-fx-domain
complexity: low
mode: autopilot
status: pending
depends_on: []
created: "2026-05-22T00:00:00Z"
---

# Work Item: Project Scaffold

## Description

Initialiser le projet Python avec uv, pyproject.toml complet (FastAPI, numpy, scipy, pydantic v2, sqlalchemy, alembic, redis, httpx, yfinance, pytest, ruff, mypy), configuration Ruff + mypy stricte, pytest config, Docker Compose skeleton (postgres + redis), GitHub Actions CI workflow de base (lint + test).

Structure cible :
```
backend/
├── app/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── api/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── regression/
├── pyproject.toml
└── Dockerfile
docker-compose.yml
.github/workflows/ci.yml
```

## Acceptance Criteria

- [ ] `uv run pytest` passe sans erreur (0 tests collectés)
- [ ] `uv run ruff check .` passe sans warning
- [ ] `uv run mypy app/` passe en mode strict
- [ ] `docker compose up -d` démarre postgres 16 + redis 7 sans erreur
- [ ] GitHub Actions workflow défini : lint (ruff + mypy) + test (pytest)
- [ ] `app/domain/__init__.py` existe — package domaine vide prêt

## Technical Notes

- uv comme package manager (pas pip/poetry)
- pyproject.toml unique à la racine de `backend/`
- Ruff rules minimales : E, F, I, N, UP, ANN
- mypy : strict = true
- Docker Compose ports : postgres=5432, redis=6379

## Dependencies

(none)
