---
id: market-data-domain
title: Market Data Domain Types & Provider Interface
intent: market-data-providers
complexity: low
mode: autopilot
status: pending
depends_on: []
created: 2026-05-25T15:45:00Z
---

# Work Item: Market Data Domain Types & Provider Interface

## Description

Définir les types du domaine pour les données de marché FX et l'interface abstraite du provider. Ces types sont la base sur laquelle tous les providers et le cache s'appuient.

## Acceptance Criteria

- [ ] `app/domain/market_data.py` définit `SpotPrice` (dataclass frozen) avec `pair`, `bid`, `ask`, `mid`, `timestamp`
- [ ] `StaleMarketDataError` et `MarketDataUnavailableError` dans `app/domain/exceptions.py`
- [ ] `app/infrastructure/providers/base.py` définit l'interface abstraite `MarketDataProvider` (ABC) avec `get_spot(pair: str) -> SpotPrice` et `get_spots(pairs: list[str]) -> dict[str, SpotPrice]`
- [ ] Tests unitaires sur `SpotPrice` (instantiation, mid calculation, staleness check)

## Technical Notes

- `SpotPrice.mid` = `(bid + ask) / 2` comme `@property`
- `SpotPrice.is_stale(max_age_seconds: int) -> bool` basé sur `timestamp`
- `MarketDataProvider` est une ABC — pas de logique métier, juste le contrat
- Utiliser `datetime` timezone-aware (UTC) pour `timestamp`

## Dependencies

(none)
