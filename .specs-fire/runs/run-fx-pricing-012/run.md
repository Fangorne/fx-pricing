---
id: run-fx-pricing-012
scope: single
work_items:
  - id: frontend-conventions-page
    intent: frontend-fx-reference
    mode: confirm
    status: completed
    current_phase: review
    checkpoint_state: approved
    current_checkpoint: plan
current_item: null
status: completed
started: 2026-05-23T11:37:52.696Z
completed: 2026-05-23T11:42:25.283Z
---

# Run: run-fx-pricing-012

## Scope
single (1 work item)

## Work Items
1. **frontend-conventions-page** (confirm) — completed


## Current Item
(all completed)

## Files Created
- `frontend/src/features/conventions/ConventionsPage.tsx`: Route page with search + list + detail
- `frontend/src/features/conventions/ConventionsList.tsx`: Filtered pair table
- `frontend/src/features/conventions/ConventionDetail.tsx`: Convention detail card
- `frontend/src/hooks/useConventions.ts`: Custom hooks for conventions fetch
- `frontend/src/features/conventions/ConventionsPage.test.tsx`: 5 Vitest + Testing Library tests

## Files Modified
- `frontend/src/App.tsx`: Added BrowserRouter + Routes + nav link
- `frontend/src/services/api.ts`: Added snake_case mapper + updated function signatures
- `frontend/src/types/fx.ts`: Aligned DayCountConvention and BusinessDayConvention values to backend
- `frontend/package.json`: Added react-router-dom v6

## Decisions
(none)


## Summary

- Work items completed: 1
- Files created: 5
- Files modified: 4
- Tests added: 5
- Coverage: 0%
- Completed: 2026-05-23T11:42:25.283Z
