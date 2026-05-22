---
id: api-fx-reference-data
title: API Backend — Endpoints Conventions & Calendriers
intent: frontend-fx-reference
complexity: medium
mode: confirm
status: pending
depends_on: [fx-conventions-table]
created: "2026-05-22T00:00:00Z"
---

# Work Item: API Backend — Endpoints Conventions & Calendriers

## Description

Créer le router FastAPI `/api/reference/` exposant les données du domaine FX en lecture seule : conventions par paire, calendriers par devise (jours fériés, is-business-day), et calcul de date spot/value. Premiers endpoints REST du projet.

Fichiers cibles :
- `backend/app/api/routers/reference.py` — router FastAPI
- `backend/app/api/schemas/reference.py` — schemas Pydantic réponse
- `backend/app/main.py` — app FastAPI avec router monté

## Acceptance Criteria

- [ ] `GET /api/reference/conventions` → liste toutes les paires avec leur convention (JSON array)
- [ ] `GET /api/reference/conventions/{pair}` → détail convention (ex: `EURUSD`) avec tous les champs
- [ ] `GET /api/reference/conventions/{pair}` paire inconnue → 404 avec message clair
- [ ] `GET /api/reference/calendars/{currency}/holidays?year=2026` → liste des jours fériés (date + nom)
- [ ] `GET /api/reference/calendars/{currency}/is-business-day?date=2026-07-04` → `{"date": "2026-07-04", "currency": "USD", "is_business_day": false, "reason": "Independence Day"}`
- [ ] `GET /api/reference/dates/spot?pair=EURUSD&trade_date=2026-05-22` → `{"spot_date": "2026-05-26"}`
- [ ] `GET /api/reference/dates/value?pair=EURUSD&trade_date=2026-05-22&tenor=3M` → `{"value_date": "2026-08-26"}`
- [ ] Swagger UI accessible sur `http://localhost:8000/docs`
- [ ] CORS configuré pour accepter `http://localhost:3000`
- [ ] Tous les endpoints retournent du JSON valide avec les bons codes HTTP

## Technical Notes

- Schemas Pydantic v2 pour les réponses (pas les modèles DB — lecture domaine uniquement)
- Appels directs aux fonctions du domaine (`get_convention()`, `get_calendar()`, `spot_date()`, `value_date()`)
- Pas de DB dans cet endpoint — données statiques du domaine
- `pair` accepté en formats : `EURUSD` ou `EUR/USD` (normalisation dans le router)

## Dependencies

- fx-conventions-table
