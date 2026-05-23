---
run: run-fx-pricing-005
work_item: fx-spot-value-dates
intent: core-fx-domain
mode: confirm
checkpoint: approved
generated: "2026-05-23T10:28:00Z"
---

# Plan: FX Spot and Value Date Generation

## Approach

`spot_date()` adds spot-lag BDs from trade date via combined calendar, then MF-adjusts.
`value_date()` dispatches on tenor category (ON/TN/SN vs. calendar periods), then BD-adjusts.
EOM rule applied when spot_date is the last BD of its month.

## Files to Create

| File | Purpose |
|------|---------|
| `backend/app/domain/date_generation.py` | `SPOT_LAGS`, `spot_date()`, `value_date()` |
| `backend/tests/unit/domain/test_date_generation.py` | Acceptance criteria + G10 coverage |

## Special Tenors

| Tenor | From | Rule |
|-------|------|------|
| ON | trade_date | +1 BD |
| TN | trade_date | +1 BD (= spot - 1 BD for T+2 pairs) |
| SN | spot_date | +1 BD |
| Weeks | spot_date | +N×7 days → adjust |
| Months/Years | spot_date | +N months (date arithmetic) → adjust |
