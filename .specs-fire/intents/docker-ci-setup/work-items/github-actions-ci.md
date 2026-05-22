---
id: github-actions-ci
title: GitHub Actions CI (lint + test)
intent: docker-ci-setup
complexity: medium
mode: confirm
status: pending
depends_on: [dockerfile-backend]
created: "2026-05-22T00:00:00Z"
---

# Work Item: GitHub Actions CI (lint + test)

## Description

Créer le workflow GitHub Actions `.github/workflows/ci.yml` avec deux jobs : `lint` (ruff check, ruff format --check, mypy strict) et `test` (pytest avec rapport de coverage). Triggered sur push et pull_request vers `main`. Cache uv pour accélérer les runs.

Fichiers cibles :
- `.github/workflows/ci.yml`

## Acceptance Criteria

- [ ] Workflow déclenché sur `push` et `pull_request` vers `main`
- [ ] Job `lint` : `uv run ruff check .` + `uv run ruff format --check .` + `uv run mypy app/` — fail fast si erreur
- [ ] Job `test` : `uv run pytest --cov=app --cov-report=xml` — fail si test échoue
- [ ] Cache uv configuré (`~/.cache/uv`) avec clé basée sur `pyproject.toml` + `uv.lock`
- [ ] `working-directory: backend` pour tous les steps
- [ ] Python 3.12 via `actions/setup-python`
- [ ] Jobs `lint` et `test` s'exécutent en parallèle
- [ ] Le workflow passe au vert sur un projet avec 0 tests (pas d'erreur "no tests collected")
- [ ] Coverage report uploadé comme artifact

## Technical Notes

- uv installé via `astral-sh/setup-uv@v3`
- `uv sync --frozen` pour reproductibilité
- `pytest --co -q` pour vérifier la collecte sans erreur avant exécution

## Dependencies

- dockerfile-backend
