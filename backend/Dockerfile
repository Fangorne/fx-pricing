# syntax=docker/dockerfile:1

# ─── Base: Python + uv ────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# ─── Dependencies layer (shared cache between dev and prod) ────────────────────
FROM base AS deps

# Copy only dependency manifests first — maximises Docker layer cache
COPY pyproject.toml uv.lock ./

# ─── Dev stage ────────────────────────────────────────────────────────────────
FROM deps AS dev

# Install all deps including dev extras
RUN uv sync --frozen --extra dev

EXPOSE 8000

# Source code is expected to be mounted as a volume in dev
CMD ["uv", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# ─── Prod stage ───────────────────────────────────────────────────────────────
FROM deps AS prod

# Install production deps only (no dev extras)
RUN uv sync --frozen --no-dev

# Copy source after deps for optimal caching
COPY app/ ./app/

EXPOSE 8000

# gunicorn with uvicorn workers — 2 workers per CPU core (tune via GUNICORN_WORKERS env)
CMD ["uv", "run", "gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
