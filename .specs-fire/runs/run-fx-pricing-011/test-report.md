# Test Report — run-fx-pricing-011

## Work Item: api-fx-reference-data

### Test Results

| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| New: `tests/integration/test_api_reference.py` | 13 | 0 | 0 |
| Existing unit tests (no regression) | 283 | 0 | 0 |
| **Total** | **296** | **0** | **0** |

### Acceptance Criteria Validation

| Criterion | Status | Notes |
|-----------|--------|-------|
| `GET /api/v1/conventions` → list all pairs | ✓ | 12 pairs, tested |
| `GET /api/v1/conventions/{pair}` → detail | ✓ | Both EURUSD and EUR/USD formats work |
| Unknown pair → 404 | ✓ | Clear error message |
| `GET /api/v1/calendars/{currency}/holidays?year=` | ✓ | USD 2026 verified |
| `GET /api/v1/calendars/{currency}/business-day?date=` | ✓ | True/false/weekend/holiday tested |
| `GET /api/v1/spot-dates/{pair}?trade_date=` | ✓ | EUR/USD T+2 with Memorial Day skip |
| `GET /api/v1/spot-dates/{pair}/value?trade_date=&tenor=` | ✓ | 3M tenor tested |
| Swagger UI on `/docs` | ✓ | FastAPI auto-generates |
| CORS for `http://localhost:3000` | ✓ | Pre-existing middleware |
| All endpoints return valid JSON + correct HTTP codes | ✓ | |

### Test Notes

- `EUR/USD` path param handled via `{pair:path}` FastAPI path converter
- Spot date test accounts for Memorial Day 2026 (May 25) — T+2 from Fri May 22 = Wed May 27
- Value date endpoint split from spot date endpoint (separate URL `/value`) for clean response model typing
