# Plan — run-fx-pricing-011

## Work Item: api-fx-reference-data
**Mode**: confirm | **Complexity**: medium

---

## Approach

Create a FastAPI router at `/api/v1/` exposing 6 read-only reference data endpoints
that delegate directly to the existing domain layer (no DB). Pydantic v2 schemas
handle JSON serialisation. Router mounted on the existing `main.py` app.

URL prefix `/api/v1/` matches what `frontend/src/services/api.ts` already calls.

## Endpoint Mapping

| Endpoint | Domain Call |
|----------|-------------|
| `GET /api/v1/conventions` | `FX_CONVENTIONS` dict |
| `GET /api/v1/conventions/{pair}` | `get_convention(pair)` |
| `GET /api/v1/calendars/{currency}/holidays?year=` | `get_calendar(currency).holidays(year)` |
| `GET /api/v1/calendars/{currency}/business-day?date=` | `get_calendar(currency).is_business_day(date)` |
| `GET /api/v1/spot-dates/{pair}?trade_date=&tenor=` | `spot_date()` + `value_date()` |

## Files to Create

- `backend/app/api/schemas/reference.py` — Pydantic v2 response schemas
- `backend/app/api/routers/reference.py` — FastAPI router (all endpoints)
- `backend/tests/test_api_reference.py` — pytest + HTTPX TestClient

## Files to Modify

- `backend/app/main.py` — include reference router with `/api/v1` prefix
