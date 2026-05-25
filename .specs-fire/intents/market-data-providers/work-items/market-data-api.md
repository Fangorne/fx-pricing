---
id: market-data-api
title: Market Data REST API Endpoints
intent: market-data-providers
complexity: medium
mode: confirm
status: pending
depends_on: [redis-price-cache]
created: 2026-05-25T15:45:00Z
---

# Work Item: Market Data REST API Endpoints

## Description

Exposer les prix spot FX via des endpoints REST. Les endpoints utilisent le `PriceCache` (avec fallback Yahoo Finance) et retournent des réponses enrichies avec l'âge de la donnée et le flag `is_stale`.

## Acceptance Criteria

- [ ] `GET /api/v1/prices/{pair}` — retourne le spot price pour une paire (ex: EUR/USD)
- [ ] `GET /api/v1/prices` — retourne les prix pour toutes les paires G10 (ou celles spécifiées via `?pairs=EUR/USD,USD/JPY`)
- [ ] Réponse inclut `bid`, `ask`, `mid`, `timestamp`, `is_stale`, `age_seconds`
- [ ] 404 si la paire n'est pas dans les conventions G10
- [ ] 503 si le provider est indisponible et le cache est vide
- [ ] Schema Pydantic `SpotPriceResponse` avec exemples
- [ ] Tag Swagger `Prices`, ajouté dans `main.py`
- [ ] Tests d'intégration avec provider mocké

## Technical Notes

- Dépendance FastAPI `get_redis()` → `redis.asyncio.Redis` (depuis `Settings.effective_redis_url`)
- Dépendance FastAPI `get_price_cache(redis=Depends(get_redis))` → `PriceCache`
- Provider `YahooFinanceProvider` instancié dans la dépendance `get_provider()`
- Valider que la paire demandée est dans `FX_CONVENTIONS` (ou `ConventionRepository`) avant de fetcher
- `age_seconds` = `(now - price.timestamp).total_seconds()`

## Dependencies

- redis-price-cache
