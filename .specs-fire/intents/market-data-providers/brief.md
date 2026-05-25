---
id: market-data-providers
title: Market Data Providers — Yahoo Finance + Redis Cache
status: planning
created: 2026-05-25T15:45:00Z
---

# Intent: Market Data Providers

## Problem

The FX Pricing platform currently has no live market data. All prices are static domain data (conventions, calendars). There is no way to fetch real-time or near-real-time FX spot prices.

## Solution

Integrate Yahoo Finance as a market data provider via `yfinance`, add a Redis cache layer with TTL and staleness detection, and expose REST endpoints for spot price queries.

## Scope

- Domain types: `SpotPrice`, `MarketDataError`, `StaleMarketDataError`
- Abstract provider interface: `MarketDataProvider` (enables future providers: Bloomberg, Refinitiv)
- Yahoo Finance adapter: fetch FX spot via `yfinance` (e.g. `EURUSD=X`)
- Redis cache: TTL-based (configurable), staleness threshold, pub/sub-ready structure
- REST API: `GET /api/v1/prices/{pair}` + `GET /api/v1/prices` (batch)

## Out of Scope

- WebSocket streaming (separate intent)
- Historical price data
- Multiple simultaneous providers with failover
