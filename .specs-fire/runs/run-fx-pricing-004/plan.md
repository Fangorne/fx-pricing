---
run: run-fx-pricing-004
work_item: fx-business-day-rules
intent: core-fx-domain
mode: confirm
checkpoint: approved
generated: "2026-05-23T10:23:00Z"
---

# Plan: Business Day Adjustment Rules

## Approach

`BusinessDayConvention` enum + pure `adjust()` function. All five conventions built on `MarketCalendar.is_business_day()`.

## Files to Create

| File | Purpose |
|------|---------|
| `backend/app/domain/business_day.py` | `BusinessDayConvention`, `adjust()` |
| `backend/tests/unit/domain/test_business_day.py` | All conventions, all acceptance criteria |

## Convention Logic

| Convention | Rule |
|------------|------|
| FOLLOWING | Next BD (may cross month) |
| MODIFIED_FOLLOWING | Next BD; if crosses month → last BD of original month |
| PRECEDING | Previous BD (may cross month) |
| MODIFIED_PRECEDING | Previous BD; if crosses month → first BD of original month |
| END_OF_MONTH | Last BD of candidate's month |
