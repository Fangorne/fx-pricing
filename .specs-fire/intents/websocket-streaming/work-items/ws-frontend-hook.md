---
id: ws-frontend-hook
title: useSpotStream React Hook
intent: websocket-streaming
complexity: medium
mode: confirm
status: pending
depends_on: [ws-backend-endpoint]
created: 2026-05-25T17:45:00Z
---

# Work Item: useSpotStream React Hook

## Description

Hook React `useSpotStream(pair: string)` qui wrape l'API native `WebSocket` du navigateur. Expose le dernier prix reçu et l'état de la connexion. Implémente un reconnect automatique avec backoff exponentiel en cas de déconnexion.

## Acceptance Criteria

- [ ] `frontend/src/hooks/useSpotStream.ts` — hook `useSpotStream(pair)`
- [ ] Retourne `{ price: SpotPrice | null, status: 'connecting' | 'live' | 'error' | 'closed' }`
- [ ] Type `SpotPrice` TypeScript : `{ pair, bid, ask, mid, timestamp, is_stale, age_seconds }`
- [ ] Reconnect automatique sur `onclose` / `onerror` avec backoff exponentiel (1s → 2s → 4s → max 30s)
- [ ] Cleanup propre sur unmount (`ws.close()`, clear timeout)
- [ ] Reconnect immédiat si `pair` change (ferme l'ancienne connexion, ouvre la nouvelle)
- [ ] URL WS construite depuis `import.meta.env.VITE_WS_URL` (défaut `ws://localhost:8000`)

## Technical Notes

- `useEffect` avec cleanup sur `pair` comme dépendance
- `useRef` pour stocker l'instance WebSocket active
- `useRef` pour stocker le timeout de reconnect (évite les memory leaks)
- Backoff : `Math.min(1000 * 2 ** attempt, 30000)`
- Sur message `{ error }` : mettre status à `'error'` sans fermer

## Dependencies

- ws-backend-endpoint
