---
run: run-fx-pricing-008
work_item: docker-compose-dev
intent: docker-ci-setup
mode: autopilot
generated: "2026-05-23T10:51:00Z"
---

# Plan: Docker Compose Dev Environment

## Files to Create

| File | Purpose |
|------|---------|
| `docker-compose.yml` | 3 services: backend (dev), postgres:16-alpine, redis:7-alpine |
| `.env.example` | Documents all required env vars |

## Files to Modify

| File | Change |
|------|--------|
| `.gitignore` | Add `.env` entry |

## Key Config

- Internal network: `fx-network`
- Backend: build target `dev`, volume `./backend:/app`, port 8000
- Postgres: named volume, healthcheck `pg_isready`, env from `.env`
- Redis: healthcheck `redis-cli ping`, port 6379
- Backend depends_on postgres+redis with `condition: service_healthy`
