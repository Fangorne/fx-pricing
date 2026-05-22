---
run: run-fx-pricing-001
work_item: project-scaffold
intent: core-fx-domain
mode: autopilot
checkpoint: none
approved_at: "2026-05-22T16:36:14Z"
---

# Implementation Plan: Project Scaffold

## Approach

Créer la structure complète du projet Python avec uv. Le backend sera dans `backend/`, avec une architecture clean (domain / application / infrastructure / api). Configuration outillage stricte (Ruff, mypy strict), pytest, Docker Compose skeleton, et GitHub Actions CI.

## Files to Create

| File | Purpose |
|------|---------|
| `backend/pyproject.toml` | Config projet uv — deps, Ruff, mypy, pytest |
| `backend/app/__init__.py` | Package app |
| `backend/app/main.py` | App FastAPI minimale |
| `backend/app/domain/__init__.py` | Package domain (vide) |
| `backend/app/application/__init__.py` | Package application (vide) |
| `backend/app/infrastructure/__init__.py` | Package infrastructure (vide) |
| `backend/app/api/__init__.py` | Package api (vide) |
| `backend/tests/__init__.py` | Package tests |
| `backend/tests/conftest.py` | Fixtures pytest de base |
| `backend/tests/unit/__init__.py` | Package unit tests |
| `backend/tests/integration/__init__.py` | Package integration tests |
| `backend/tests/regression/__init__.py` | Package regression tests |
| `docker-compose.yml` | Skeleton postgres + redis |
| `.github/workflows/ci.yml` | CI lint + test |
| `.gitignore` | Ignores Python, uv, Docker |

## Files to Modify

| File | Changes |
|------|---------|
| (none) | |

## Tests

| Test File | Coverage |
|-----------|----------|
| `backend/tests/conftest.py` | Fixtures — pas de tests fonctionnels à ce stade |

---
*Plan approved at checkpoint. Execution follows.*
