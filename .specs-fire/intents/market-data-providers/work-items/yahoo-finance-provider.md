---
id: yahoo-finance-provider
title: Yahoo Finance Provider Adapter
intent: market-data-providers
complexity: medium
mode: confirm
status: pending
depends_on: [market-data-domain]
created: 2026-05-25T15:45:00Z
---

# Work Item: Yahoo Finance Provider Adapter

## Description

Implémenter l'adaptateur Yahoo Finance qui implémente `MarketDataProvider`. Yahoo Finance expose les taux FX sous le format `EURUSD=X` via `yfinance.Ticker`. L'adaptateur gère le mapping paire → ticker, les erreurs réseau, et les données manquantes.

## Acceptance Criteria

- [ ] `app/infrastructure/providers/yahoo_finance.py` implémente `YahooFinanceProvider(MarketDataProvider)`
- [ ] `get_spot(pair)` — fetch un taux FX spot (bid/ask/mid) depuis Yahoo Finance
- [ ] `get_spots(pairs)` — fetch plusieurs paires en parallèle (asyncio.gather)
- [ ] Mapping `EUR/USD` → `EURUSD=X`, `USD/JPY` → `JPYUSD=X` (conventions Yahoo)
- [ ] Erreur réseau ou donnée manquante → `MarketDataUnavailableError`
- [ ] Tests unitaires avec `httpx` mock ou `yfinance` patché

## Technical Notes

- `yfinance.Ticker("EURUSD=X").fast_info` ou `.history(period="1d", interval="1m").iloc[-1]`
- Yahoo retourne bid/ask séparément via `.fast_info.bid` / `.fast_info.ask` — fallback sur `last_price` si bid/ask absents
- Wrapper async : `asyncio.get_event_loop().run_in_executor(None, sync_fetch)` ou `anyio.to_thread.run_sync`
- Timeout configurable (défaut 5s) via `Settings`

## Dependencies

- market-data-domain
