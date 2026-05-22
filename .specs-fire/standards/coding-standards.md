# Coding Standards

## Overview

Standards pour le projet FX Pricing : backend Python (domain-driven, clean architecture) et frontend TypeScript (React). L'accent est mis sur la précision des calculs financiers, la clarté du domaine FX, et la séparation stricte des couches.

## Code Formatting

**Backend Tool**: Ruff format
**Config**: pyproject.toml `[tool.ruff.format]`
**Frontend Tool**: Prettier 3
**Config**: .prettierrc
**Enforcement**: Pre-commit hook + CI gate

### Key Settings

- **Line length**: 100 (backend) / 100 (frontend)
- **Quotes**: Double (Python) / Single (TypeScript)
- **Trailing commas**: Yes (both)

## Linting

**Backend Tool**: Ruff
**Base Config**: pyproject.toml `[tool.ruff.lint]`
**Strictness**: Strict — rules E, F, I, N, UP, ANN pour le domaine financier

**Frontend Tool**: ESLint 9 (flat config)
**Base Config**: eslint.config.js
**Strictness**: Strict TypeScript rules

### Key Rules

- `ANN` (type annotations): error — toutes les fonctions publiques typées
- `N803/N806` (naming): error — conventions Python strictes
- `no-any`: error (TypeScript) — pas de `any` dans le domaine FX
- `strict-boolean-expressions`: error — éviter les erreurs de comparaison sur notionals

## Naming Conventions

### Variables and Functions

| Element | Convention | Example |
|---------|------------|---------|
| Variables Python | snake_case | `spot_rate`, `forward_points` |
| Fonctions Python | snake_case | `calculate_forward_rate()` |
| Classes Python | PascalCase | `FXConvention`, `PricingEngine` |
| Constantes Python | SCREAMING_SNAKE | `MAX_TENOR_DAYS`, `DEFAULT_SPOT_LAG` |
| Variables TS | camelCase | `spotRate`, `forwardPoints` |
| Fonctions TS | camelCase | `calculateForwardRate()` |
| Composants React | PascalCase | `FXTicket`, `PricingDashboard` |
| Types/Interfaces TS | PascalCase | `FXQuote`, `PricingResult` |
| Hooks React | camelCase + `use` prefix | `useFXStream`, `usePricingEngine` |

### Files and Folders

- **Python modules**: snake_case (e.g., `fx_conventions.py`, `pricing_engine.py`)
- **Python packages**: snake_case (e.g., `market_data/`, `pricing/`)
- **TypeScript components**: PascalCase (e.g., `FXTicket.tsx`)
- **TypeScript hooks/utils**: camelCase (e.g., `useFXStream.ts`, `formatRate.ts`)

## File Organization

### Project Structure

```
fx-pricing/
├── backend/
│   ├── app/
│   │   ├── domain/              # Entités et règles métier FX pures
│   │   │   ├── conventions/     # FXConvention, SpotLag, DayCount
│   │   │   ├── calendars/       # MarketCalendar, HolidayRule
│   │   │   ├── pricing/         # PricingEngine, BlackScholes, Greeks
│   │   │   └── market_data/     # MarketDataPort (interface)
│   │   ├── application/         # Use cases / services
│   │   ├── infrastructure/      # Providers, DB, Cache
│   │   │   ├── providers/       # YahooFinanceProvider, etc.
│   │   │   └── persistence/     # SQLAlchemy repos
│   │   └── api/                 # FastAPI routers + WebSocket handlers
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/          # Composants React réutilisables
│   │   ├── features/            # Features FX (pricing, booking, charts)
│   │   ├── hooks/               # Custom hooks (useFXStream, usePricing)
│   │   ├── store/               # Zustand stores
│   │   └── types/               # Types TypeScript domaine FX
│   └── package.json
└── docker-compose.yml
```

### Conventions

- **Domain isolation**: Le domaine (`domain/`) ne dépend d'aucune infrastructure
- **Provider pattern**: Toute dépendance externe passe par une interface (`Port`) dans le domaine
- **Stateless pricing**: Les fonctions de calcul sont des fonctions pures sans side effects
- **Decimal precision**: Utiliser `Decimal` Python pour les notionals, `float64` numpy pour les calculs de courbes

## Import Order

```python
# 1. Stdlib
import datetime
from decimal import Decimal

# 2. Third-party
import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel

# 3. Internal — domain first, then infrastructure
from app.domain.conventions import FXConvention
from app.infrastructure.providers import YahooFinanceProvider
```

**Rules**:
- Ruff `isort` enforced — ordre automatique
- Pas d'import circulaire entre couches (domain ← application ← infrastructure)
- Imports absolus uniquement (pas de `..`)

## Error Handling

### Pattern

**Approach**: Exception hiérarchique domaine + HTTP exception mapping dans l'API layer

### Guidelines

- Définir des exceptions domaine explicites (`InvalidCurrencyPair`, `StaleMarketDataError`, `UnsupportedTenorError`)
- Ne jamais laisser remonter les exceptions infrastructure brutes dans le domaine
- L'API layer traduit les exceptions domaine en codes HTTP appropriés (400, 422, 503)
- Les erreurs de calcul financier sont loggées avec le contexte complet (paire, ténor, date)

### Example

```python
# Domaine — exception métier explicite
class StaleMarketDataError(FXPricingError):
    def __init__(self, pair: str, age_seconds: int) -> None:
        self.pair = pair
        self.age_seconds = age_seconds
        super().__init__(f"Market data for {pair} is {age_seconds}s old")

# API layer — mapping HTTP
@app.exception_handler(StaleMarketDataError)
async def stale_data_handler(request: Request, exc: StaleMarketDataError):
    return JSONResponse(status_code=503, content={"error": "stale_data", "pair": exc.pair})
```

## Logging

**Tool**: structlog (structured logging JSON)
**Format**: JSON en production, colored console en dev

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Calculs intermédiaires (interpolation, discount factors) |
| INFO | Prix calculés, connexions WebSocket, cache hits/misses |
| WARNING | Données stale, fallback provider, latence anormale |
| ERROR | Erreur provider, calcul impossible, DB indisponible |
| CRITICAL | Moteur de pricing hors service |

### Guidelines

**Always log**:
- Chaque requête de pricing avec paire + ténor + produit
- Connexion/déconnexion WebSocket avec subscription info
- Cache miss sur market data avec staleness
- Erreurs provider avec détail

**Never log**:
- Credentials ou tokens
- Données utilisateur sensibles
- Valeurs intermédiaires des calculs en production (verbosité)

## Comments and Documentation

### When to Comment

- Formules financières non triviales (Black-Scholes, interpolation log-linéaire)
- Conventions de marché spécifiques à une devise (ex: USD/JPY T+2 sauf certains jours)
- Workarounds pour des limitations de providers (ex: Yahoo Finance lag)
- Invariants de précision numérique importants

### Documentation Format

**Functions**: Docstring Google style pour les fonctions publiques du domaine
**Classes**: Docstring courte décrivant la responsabilité domaine

---
*Generated by specs.md - fabriqa.ai FIRE Flow*
