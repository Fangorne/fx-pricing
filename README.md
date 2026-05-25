# FX Pricing Platform

Terminal de référence FX à destination des traders — conventions de marché, calendriers, et calculateur de dates spot/valeur pour les paires G10.

## Stack

| Couche | Technologie |
|--------|-------------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend | FastAPI + Python 3.12 + SQLAlchemy (async) |
| Base de données | PostgreSQL 16 |
| Cache | Redis 7 |
| Package manager (Python) | uv |
| Package manager (JS) | pnpm |

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/) avec les extensions Python et ESLint
- Node.js 20+ et pnpm (`npm install -g pnpm`)
- Python 3.12+ et uv (`pip install uv`)

## Démarrage rapide

```bash
# 1. Variables d'environnement
cp .env.example .env

# 2. Démarrer l'infra (PostgreSQL + Redis)
docker compose up -d postgres redis

# 3. Backend
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000

# 4. Frontend (autre terminal)
cd frontend
pnpm install
pnpm dev
```

- Frontend : http://localhost:5173
- API : http://localhost:8000
- Docs API : http://localhost:8000/docs

## Développement avec VS Code

Ouvrir le projet à la racine, puis `F5` → **🚀 Full Stack (debug)**.

Docker Desktop doit être démarré. La configuration lance automatiquement l'infra Docker, le backend FastAPI avec les breakpoints Python actifs, et le frontend Vite.

**Configurations de debug disponibles :**

| Configuration | Usage |
|---------------|-------|
| `🚀 Full Stack (debug)` | Backend + Frontend en une fois |
| `Backend: FastAPI (debug)` | Backend seul avec breakpoints |
| `Backend: pytest (debug)` | Tests avec breakpoints |
| `Frontend: Chrome (attach)` | Breakpoints TypeScript/React dans Chrome |

**Tasks disponibles** (`Ctrl+Shift+P` → Tasks: Run Task) :

| Task | Usage |
|------|-------|
| `infra: up` | Démarre PostgreSQL + Redis |
| `infra: down` | Arrête les conteneurs |
| `infra: logs` | Logs de l'infra en temps réel |
| `fullstack: start (no debug)` | Tout lancer sans debugger |

## Structure du projet

```
fx-pricing/
├── backend/
│   ├── app/
│   │   ├── api/            # Routes FastAPI
│   │   ├── application/    # Use cases / services
│   │   ├── domain/         # Entités et règles métier
│   │   └── infrastructure/ # BDD, cache, adaptateurs externes
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # Composants UI réutilisables
│   │   ├── features/       # Pages par domaine fonctionnel
│   │   └── contexts/       # Contextes React (thème…)
│   └── package.json
├── docker-compose.yml
└── .env.example
```

## Commandes utiles

```bash
# Backend — tests
cd backend && uv run pytest -xvs

# Backend — lint
cd backend && uv run ruff check .

# Frontend — build de production
cd frontend && pnpm build

# Docker — stack complète
docker compose --profile full up -d

# Docker — tout arrêter
docker compose down
```
