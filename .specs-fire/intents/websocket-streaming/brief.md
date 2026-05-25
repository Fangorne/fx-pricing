---
id: websocket-streaming
title: WebSocket Streaming — Live FX Spot Prices
status: in_progress
created: 2026-05-25T17:45:00Z
---

# Intent: WebSocket Streaming — Live FX Spot Prices

## Goal

Stream live FX spot prices over WebSocket from the FastAPI backend and display a real-time price widget on the frontend for a user-selected currency pair.

## Users

Traders and users of the FX Pricing dashboard who need live, push-based price updates without manual refresh or polling.

## Problem

The current REST endpoint `GET /api/v1/prices/{pair}` requires the client to poll for new data. There is no push mechanism, no visual live feel, and no way to see prices update continuously in the UI.

## Success Criteria

- Backend exposes `WS /ws/prices/{pair}` and pushes a new SpotPrice JSON every 5 seconds (configurable)
- Frontend `useSpotStream(pair)` hook consumes the WebSocket and exposes the latest price + connection state
- A live price widget shows bid / ask / mid with a visual flash animation on each price update
- User can select which pair to watch from a dropdown (all G10 pairs)
- Connection drops are handled with automatic exponential-backoff reconnect
- Disconnected / stale state is clearly visible in the UI (e.g. grey badge, "reconnecting…")

## Constraints

- Reuses existing `PriceCache` + `YahooFinanceProvider` stack — no new data source
- FastAPI native WebSocket (no Socket.io, no external broker)
- Frontend uses native browser `WebSocket` API wrapped in a React hook
- Push interval configurable via `Settings.ws_price_interval_seconds` (default 5s)

## Notes

(none)
