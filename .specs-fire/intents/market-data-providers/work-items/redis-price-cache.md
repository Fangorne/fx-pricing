---
id: redis-price-cache
title: Redis Price Cache Layer
intent: market-data-providers
complexity: medium
mode: confirm
status: pending
depends_on: [yahoo-finance-provider]
created: 2026-05-25T15:45:00Z
---

# Work Item: Redis Price Cache Layer

## Description

Ajouter une couche de cache Redis entre l'API et le provider Yahoo Finance. Le cache stocke les `SpotPrice` sérialisés en JSON avec un TTL configurable. Si la donnée est absente ou expirée, le cache va chercher via le provider et met à jour Redis.

## Acceptance Criteria

- [ ] `app/infrastructure/cache/price_cache.py` — `PriceCache` avec `get(pair)` et `set(pair, price)` et `get_or_fetch(pair, provider)`
- [ ] TTL configurable via `Settings.market_data_cache_ttl_seconds` (défaut 30s)
- [ ] Staleness threshold séparé `Settings.market_data_stale_threshold_seconds` (défaut 60s)
- [ ] `get_or_fetch` : hit cache → retourne directement ; miss → appelle provider → stocke → retourne
- [ ] Si provider échoue et cache contient une valeur expirée → retourne la valeur avec `is_stale=True` (graceful degradation)
- [ ] Tests unitaires avec `fakeredis` (async)

## Technical Notes

- Clé Redis : `fx:spot:{pair}` (ex: `fx:spot:EUR/USD`)
- Valeur : JSON `{"bid": 1.0850, "ask": 1.0852, "mid": 1.0851, "timestamp": "2026-05-25T15:30:00Z"}`
- Client Redis async : `redis.asyncio.Redis` (déjà dans les deps)
- Ajouter `fakeredis` aux dev deps pour les tests
- `PriceCache` reçoit `redis.asyncio.Redis` en injection (pas de singleton)

## Dependencies

- yahoo-finance-provider
