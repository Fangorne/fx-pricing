# Testing Standards

## Overview

Stratégie de test pour FX Pricing : priorité aux tests quantitatifs (non-régression pricing), tests d'intégration des providers market data, et tests E2E des flux WebSocket temps réel. La précision des calculs financiers est un critère de qualité bloquant.

## Testing Framework

**Backend Framework**: pytest 8 + pytest-asyncio
**Frontend Framework**: Vitest 1.6
**E2E Framework**: Playwright 1.44
**Runner**: pytest (backend) / vitest (frontend)

## Test Types

| Type | Tool | Location | When to Use |
|------|------|----------|-------------|
| Unit (calculs FX) | pytest | `backend/tests/unit/` | Fonctions pricing pures, conventions, calendriers |
| Unit (composants) | Vitest + RTL | `frontend/src/**/__tests__/` | Composants React, hooks, stores |
| Integration (API) | pytest + httpx | `backend/tests/integration/` | Endpoints REST, auth, DB |
| Integration (WS) | pytest + websockets | `backend/tests/integration/` | Streaming, subscriptions |
| Regression pricing | pytest | `backend/tests/regression/` | Non-régression sur valeurs de référence |
| Mutation testing | mutmut | `backend/tests/unit/` | Vérifier la qualité des assertions sur le domaine FX |
| E2E | Playwright | `e2e/` | Flux complets : ticket FX → prix → booking |

## Coverage Requirements

**Target**: 85%
**Enforcement**: CI gate bloquant — PR rejetée si < 85% sur `domain/` et `application/`

**Critical paths that MUST have coverage:**
- Calcul forward rate (toutes conventions de paires)
- Calcul Black-Scholes FX + Greeks (delta, gamma, vega, theta)
- Interpolation courbes de taux (log-linéaire, cubic spline)
- Business day adjustment (Following, Modified Following, Preceding)
- Génération dates spot/value par paire/calendrier
- Validation conventions (paire, ténor, notional, sens cotation)
- Cache staleness et fallback provider

## Test Naming

**Pattern**: `test_<what>_<condition>_<expected_result>`

**Examples**:
- `test_forward_rate_eurusd_6m_matches_reference_value` — pricing de référence
- `test_spot_lag_usdjpy_returns_t_plus_2` — convention de marché
- `test_black_scholes_atm_call_delta_is_approximately_05` — Greeks
- `test_calendar_usd_excludes_thanksgiving` — jours fériés
- `test_stale_data_raises_stale_market_data_error` — gestion qualité données

## Test Structure

```python
# Arrange - Act - Assert, données de référence explicites
def test_forward_rate_eurusd_3m_matches_reference() -> None:
    # Arrange
    spot = 1.0850
    domestic_rate = 0.045  # EUR 3M
    foreign_rate = 0.053   # USD 3M
    days = 91

    # Act
    result = calculate_forward_rate(spot, domestic_rate, foreign_rate, days)

    # Assert — tolérance financière explicite (1 pip = 0.0001)
    assert abs(result - 1.0780) < 0.0001, f"Forward rate {result} hors tolérance"
```

## Mock Strategy

**Approach**: Mocks uniquement aux frontières d'infrastructure — jamais dans le domaine

**Guidelines**:
- Mocker les providers market data (Yahoo Finance) avec des fixtures de données réelles
- Ne jamais mocker les fonctions de calcul financier — les tester avec des valeurs de référence
- Utiliser des fixtures pytest pour les calendriers et conventions standard
- Les tests d'intégration utilisent une vraie DB PostgreSQL de test (Docker)
- Redis de test isolé par test via `fakeredis` en unit, réel en intégration

## Test Data

**Strategy**: Fixtures de données de marché réelles horodatées comme référence

**Guidelines**:
- Maintenir un fichier `tests/fixtures/reference_prices.json` avec des prix de marché validés
- Les tests de régression comparent toujours avec ces valeurs de référence
- Tolérance numérique explicite dans chaque assertion de prix (en pips)
- Données de calendriers issues de sources officielles (calendriers FED, BCE, BOJ)
- Ne jamais utiliser `random` dans les tests de pricing

## Mutation Testing

**Tool**: mutmut
**Scope**: `backend/app/domain/` uniquement — le domaine FX est le périmètre critique
**Target mutation score**: ≥ 80% sur `domain/`

**Rationale**: La couverture de ligne mesure l'exécution du code, pas la qualité des assertions. Le mutation testing détecte les assertions trop permissives (ex. `assert result is not None` au lieu de vérifier la valeur exacte). Critique pour les calculs financiers où une assertion faible peut masquer une régression de 10 pips.

**Focus modules** (par ordre de priorité) :
1. `app/domain/conventions.py` — DayCountBasis, FXConvention
2. `app/domain/business_day.py` — adjust(), Modified Following
3. `app/domain/date_generation.py` — spot_date(), value_date()
4. `app/domain/calendar.py` — is_business_day(), holidays()

**Configuration** (`pyproject.toml`) :
```toml
[tool.mutmut]
paths_to_mutate = "app/domain/"
tests_dir = "tests/unit/"
```

**CI**: Non-bloquant en PR (coût CPU) — run hebdomadaire via GitHub Actions schedule. Bloquant uniquement si le score tombe sous 70%.

## Running Tests

```bash
# Run all tests
cd backend && uv run pytest

# Run with coverage
cd backend && uv run pytest --cov=app --cov-report=html

# Run specific test file
cd backend && uv run pytest tests/unit/pricing/test_forward_rate.py

# Run regression tests only
cd backend && uv run pytest tests/regression/ -v

# Run in watch mode
cd backend && uv run pytest-watch

# Mutation testing (domaine FX uniquement)
cd backend && uv run mutmut run
uv run mutmut results          # résumé
uv run mutmut show <id>        # voir le mutant survivant

# Frontend tests
cd frontend && pnpm test

# E2E tests
pnpm playwright test
```

## CI/CD Integration

**Pipeline**: GitHub Actions
**Trigger**: Push + Pull Request vers main

**Required gates**:
- Tests unitaires domaine (100% pass)
- Tests de régression pricing (0 régression tolérée)
- Coverage ≥ 85% sur domain/ et application/
- Linting Ruff + ESLint (0 erreur)
- Type checking mypy (strict) + tsc (strict)

---
*Generated by specs.md - fabriqa.ai FIRE Flow*
