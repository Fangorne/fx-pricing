---
id: ws-backend-endpoint
title: WebSocket Backend Endpoint
intent: websocket-streaming
complexity: medium
mode: confirm
status: pending
depends_on: []
created: 2026-05-25T17:45:00Z
---

# Work Item: WebSocket Backend Endpoint

## Description

Implémenter `WS /ws/prices/{pair}` dans FastAPI. Le endpoint accepte une connexion WebSocket, valide la paire, puis loop en envoyant le prix spot JSON toutes les `ws_price_interval_seconds` secondes via `PriceCache.get_or_fetch()`. Gère proprement la déconnexion client et les erreurs provider.

## Acceptance Criteria

- [ ] `app/api/routers/ws_prices.py` — WebSocket router avec `WS /ws/prices/{pair}`
- [ ] Validation de la paire au moment du handshake — ferme avec code 4004 si inconnue
- [ ] Loop de push toutes les `Settings.ws_price_interval_seconds` secondes (défaut 5s)
- [ ] Payload JSON : `{"pair", "bid", "ask", "mid", "timestamp", "is_stale", "age_seconds"}`
- [ ] Déconnexion client (WebSocketDisconnect) → sortie propre de la loop
- [ ] Erreur provider → envoie `{"error": "...", "pair": "..."}` et continue (ne ferme pas la connexion)
- [ ] `Settings.ws_price_interval_seconds: int = 5` ajouté à `config.py`
- [ ] Tests : `pytest-anyio` ou `starlette.testclient` WebSocket test client

## Technical Notes

- `from fastapi import WebSocket, WebSocketDisconnect`
- `asyncio.sleep(settings.ws_price_interval_seconds)` entre chaque push
- Dépendances injectées via `Depends` ou instanciées directement (WS ne supporte pas tous les Depends)
- Ajouter le router dans `main.py` (pas de prefix `/api/v1` — WS à la racine `/ws`)

## Dependencies

(none)
