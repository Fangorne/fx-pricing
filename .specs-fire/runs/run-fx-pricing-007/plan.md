---
run: run-fx-pricing-007
work_item: dockerfile-backend
intent: docker-ci-setup
mode: autopilot
generated: "2026-05-23T10:41:00Z"
---

# Plan: Dockerfile Backend Multi-Stage

## Approach

Two-stage Dockerfile: `dev` with hot-reload via uvicorn, `prod` with gunicorn+uvicorn workers.
Layer ordering: install uv → copy lock files → install deps → copy source code (maximises Docker cache hits).

## Files to Create

| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Multi-stage dev + prod |
| `backend/.dockerignore` | Exclude venv, caches, tests |

## Files to Modify

None.

## Tests

Docker build commands (CI-verified, not pytest). No pytest tests for Dockerfile.
