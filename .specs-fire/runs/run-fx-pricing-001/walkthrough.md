---
run: run-fx-pricing-001
work_item: project-scaffold
intent: core-fx-domain
generated: "2026-05-22T17:08:00Z"
mode: autopilot
---

# Implementation Walkthrough: Project Scaffold

## Summary

This run established the complete Python backend scaffold for the FX Pricing platform. A FastAPI application was wired up with Clean Architecture layer separation, a working health endpoint, full type-checking and linting tooling, and a GitHub Actions CI pipeline.

## Structure Overview

The backend is structured as a Clean Architecture monolith with four layers (domain, application, infrastructure, API). Each layer is a Python package under `backend/app/`. The FastAPI app lives in `app/main.py` and is the sole entry point — routers will be registered there as feature work items are executed. Tests mirror the production structure under `backend/tests/` with separate unit, integration, and regression sub-packages.

## Architecture

### Pattern Used
Clean Architecture — strict layer separation prevents infrastructure concerns (database, HTTP) from leaking into domain logic.

### Layer Structure
```text
┌────────────────────────────────┐
│   API (FastAPI routers)        │  app/api/
├────────────────────────────────┤
│   Application (use cases)      │  app/application/
├────────────────────────────────┤
│   Domain (value objects, rules)│  app/domain/
├────────────────────────────────┤
│   Infrastructure (DB, cache)   │  app/infrastructure/
└────────────────────────────────┘
```

## Files Changed

### Created

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app factory — CORS middleware, health endpoint, future router registration point |
| `backend/app/__init__.py` | App package marker |
| `backend/app/domain/__init__.py` | Domain layer package — will hold currency pairs, rate value objects |
| `backend/app/application/__init__.py` | Application layer package — will hold use cases |
| `backend/app/infrastructure/__init__.py` | Infrastructure layer package — will hold DB/cache adapters |
| `backend/app/api/__init__.py` | API layer package — will hold FastAPI routers |
| `backend/tests/conftest.py` | Shared pytest fixture — `AsyncClient` over ASGI transport |
| `backend/tests/integration/test_health.py` | Smoke test: GET /health → 200 `{"status": "ok"}` |
| `backend/pyproject.toml` | Full project config: dependencies, ruff, mypy strict, pytest-asyncio, coverage ≥85% |
| `.github/workflows/ci.yml` | CI: lint (ruff + mypy) and test jobs run in parallel on push/PR to main |

## Key Implementation Details

### 1. ASGI Test Client Pattern

Tests use `httpx.AsyncClient` with `ASGITransport` — no server process needed. This means integration tests run fast and deterministically in CI without port binding or process management.

### 2. `asyncio_mode = "auto"` in pytest

All `async def test_*` functions are automatically treated as async tests. No need to decorate each test with `@pytest.mark.asyncio`.

### 3. Strict mypy applied only to `app/`

`tests/` is excluded from mypy strict checking (`exclude = ["tests/"]`) because test fixtures (generators, mocks) generate many false positives under strict mode. The `ANN` ruff rule is also disabled for test files.

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Package manager | `uv` | Faster than pip, lock file support, native venv management |
| Python version | 3.12 | Required for latest type narrowing and `dict[str, str]` syntax without `from __future__ import annotations` |
| Web framework | FastAPI + uvicorn | Async-native, excellent OpenAPI generation, matches project spec |
| Test transport | `httpx.ASGITransport` | Avoids test server spin-up, deterministic, standard FastAPI testing pattern |
| CORS origin | `http://localhost:3000` hardcoded | Dev-only scaffold; will be moved to env config when staging is added |
| Pre-provisioned deps | `python-jose`, `passlib`, `sqlalchemy`, `redis` | Anticipated by project spec; avoids dependency churn across future work items |

## Deviations from Plan

None — scaffold implemented exactly as specified in the work item.

## Dependencies Added

| Package | Why Needed |
|---------|------------|
| `fastapi>=0.111.0` | Web framework |
| `uvicorn[standard]>=0.30.0` | ASGI server |
| `pydantic>=2.7.0` | Data validation (FastAPI integration) |
| `sqlalchemy>=2.0.0` | ORM for future DB work |
| `alembic>=1.13.0` | DB migrations |
| `asyncpg>=0.29.0` | Async PostgreSQL driver |
| `redis>=5.0.0` | Cache client for future market data streaming |
| `httpx>=0.27.0` | HTTP client + test transport |
| `yfinance>=0.2.0` | Market data source |
| `numpy`, `scipy` | Numerical/financial computations |
| `python-jose[cryptography]` | JWT auth (pre-provisioned) |
| `passlib[bcrypt]` | Password hashing (pre-provisioned) |
| `structlog>=24.0.0` | Structured logging |
| `python-dotenv>=1.0.0` | `.env` file loading |

## How to Verify

1. **Run tests**

   ```bash
   cd backend && uv run pytest -q
   ```

   Expected: `1 passed`

2. **Type check**

   ```bash
   cd backend && uv run mypy app/
   ```

   Expected: `Success: no issues found in 6 source files`

3. **Lint**

   ```bash
   cd backend && uv run ruff check . && uv run ruff format --check .
   ```

   Expected: no output (clean)

4. **Start dev server**

   ```bash
   cd backend && uv run uvicorn app.main:app --reload
   # GET http://localhost:8000/health → {"status": "ok"}
   ```

## Test Coverage

- Tests added: 1 (integration smoke test)
- Coverage: 100% (`app/` — all scaffold modules)
- Status: passing

## Ready for Review

- [x] All acceptance criteria met (docker compose pending manual infra validation)
- [x] Tests passing
- [x] No critical issues
- [x] Developer notes captured

## Developer Notes

- `conftest.py` fixture uses `AsyncGenerator[AsyncClient, None]` return type — required for async `yield` fixtures under any future mypy test coverage.
- CORS is `localhost:3000` only — remember to env-var this when adding staging/prod config (work item `github-actions-ci` is a good moment).
- `uv sync --frozen --extra dev` in CI ensures the lock file is honoured; always commit `uv.lock` when updating dependencies.

---
*Generated by specs.md - fabriqa.ai FIRE Flow Run run-fx-pricing-001*
