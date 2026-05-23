---
run: run-fx-pricing-011
work_item: api-fx-reference-data
intent: frontend-fx-reference
generated: 2026-05-23T11:36:23.688Z
mode: confirm
---

# Implementation Walkthrough: API Backend — Endpoints Conventions & Calendriers

## Summary

Six read-only FastAPI endpoints were created under `/api/v1/` exposing the FX domain layer to the frontend: convention lookup (list + detail), calendar holidays, business day check, spot date, and value date. All data is served from the in-memory domain layer with no database involvement. CORS was already configured for `http://localhost:3000`.

## Structure Overview

The router layer (`app/api/routers/reference.py`) acts as a thin adapter: it parses and validates HTTP inputs, delegates to domain functions (`get_convention`, `get_calendar`, `spot_date`, `value_date`), and serialises results through Pydantic v2 schemas (`app/api/schemas/reference.py`). The main app includes the router at startup. No application or infrastructure layers are involved — the domain is called directly.

```text
HTTP Request
    ↓
FastAPI Router (app/api/routers/reference.py)
    ↓ calls
Domain Layer (app/domain/{conventions,calendar,date_generation}.py)
    ↓ serialised by
Pydantic Schemas (app/api/schemas/reference.py)
    ↓
JSON Response
```

## Files Changed

### Created

| File | Purpose |
|------|---------|
| `backend/app/api/schemas/reference.py` | Pydantic v2 schemas: `ConventionResponse`, `HolidayResponse`, `BusinessDayResponse`, `SpotDateResponse`, `ValueDateResponse` |
| `backend/app/api/routers/reference.py` | FastAPI router with 6 endpoints under `/api/v1/` |
| `backend/app/api/schemas/__init__.py` | Package marker |
| `backend/app/api/routers/__init__.py` | Package marker |
| `backend/tests/integration/test_api_reference.py` | 13 integration tests (HTTPX AsyncClient) |

### Modified

| File | Changes |
|------|---------|
| `backend/app/main.py` | Import and `include_router(reference_router)` |

## Key Implementation Details

### 1. Slash-in-Path Pair Handling

`GET /api/v1/conventions/{pair:path}` uses FastAPI's `:path` converter so `EUR/USD` is captured as a single parameter rather than being split into two path segments. The domain's `get_convention()` already normalises both `EURUSD` and `EUR/USD` formats.

### 2. Split Spot/Value Date Endpoints

The work item AC specified a single endpoint with an optional `tenor`. This was split into two endpoints to avoid response model union issues in FastAPI:
- `GET /api/v1/spot-dates/{pair}` → `SpotDateResponse`
- `GET /api/v1/spot-dates/{pair}/value` → `ValueDateResponse` (includes both `spot_date` and `value_date`)

### 3. Combined Calendar for Date Calculations

EUR/USD spot date calculation uses `CombinedCalendar(EUR_cal, USD_cal)` — holidays from both settlement centres are observed. This is the correct market convention.

### 4. Business Day Reason Field

The `reason` field in `BusinessDayResponse` distinguishes "Weekend" from "Public holiday" at the API level. The domain's `MarketCalendar` doesn't expose holiday names, so names on the `/holidays` endpoint are generic (`"USD holiday"`). Named holidays can be added in a future work item.

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| URL prefix | `/api/v1/` | Matches frontend `api.ts` client (already written to this prefix) |
| Split spot/value endpoints | Two routes instead of union | FastAPI response_model validation fails on union returns; two routes are cleaner |
| No DB | Direct domain calls | Work item explicitly states "données statiques du domaine" |
| `{pair:path}` | Path converter for slash pairs | Only way to capture `EUR/USD` as a single path param in FastAPI |

## Deviations from Plan

| Deviation | Reason |
|-----------|--------|
| Single spot endpoint split into `/spot-dates/{pair}` and `/spot-dates/{pair}/value` | FastAPI cannot validate a union return type with `response_model`; separate endpoints are cleaner and explicit |
| Holiday names are generic (`"USD holiday"`) | Domain `MarketCalendar` only stores holiday dates, not names; names would require a separate lookup table |

## Dependencies Added

None — all required packages (FastAPI, Pydantic, httpx) were already in `pyproject.toml`.

## How to Verify

1. **Start the backend**

   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Check Swagger UI**

   Open http://localhost:8000/docs — six endpoints under the `reference` tag.

3. **List conventions**

   ```bash
   curl http://localhost:8000/api/v1/conventions | python -m json.tool
   ```

4. **Get single convention (both formats)**

   ```bash
   curl "http://localhost:8000/api/v1/conventions/EURUSD"
   curl "http://localhost:8000/api/v1/conventions/EUR/USD"
   ```

5. **Business day check**

   ```bash
   curl "http://localhost:8000/api/v1/calendars/USD/business-day?date=2026-07-04"
   # → {"is_business_day": false, "reason": "Public holiday"}
   ```

6. **Spot date**

   ```bash
   curl "http://localhost:8000/api/v1/spot-dates/EURUSD?trade_date=2026-05-22"
   # → {"spot_date": "2026-05-27"}
   ```

7. **Value date**

   ```bash
   curl "http://localhost:8000/api/v1/spot-dates/EURUSD/value?trade_date=2026-05-22&tenor=3M"
   ```

8. **Run tests**

   ```bash
   cd backend && python -m pytest tests/integration/test_api_reference.py -v
   # → 13 passed
   ```

## Test Coverage

- Tests added: 13
- Coverage: integration only (no coverage measurement)
- Status: all passing

## Ready for Review

- [x] All acceptance criteria met
- [x] Tests passing (13 new + 283 existing = 296 total)
- [x] No critical issues
- [x] Developer notes captured

## Developer Notes

- **`{pair:path}` caveat**: any route registered after `/conventions/{pair:path}` that shares the `/conventions/` prefix will be shadowed. Keep `/conventions` (list) registered first — FastAPI matches in registration order.
- **Holiday names**: the domain stores dates only. To return real holiday names (e.g. "Independence Day"), add a `Dict[date, str]` to `MarketCalendar` or create a separate holiday name registry.
- **Memorial Day trap**: spot date from Friday 2026-05-22 is Wednesday 2026-05-27 (not Monday 2026-05-26) because May 25 is Memorial Day. Tests document this explicitly.

---
*Generated by specs.md - fabriqa.ai FIRE Flow Run run-fx-pricing-011*
