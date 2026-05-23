# Plan — run-fx-pricing-014

## Work Item: frontend-spot-calculator
**Mode**: confirm | **Complexity**: medium

---

## Approach

Build `/dates` route: pair selector + trade date + tenor selector, auto-calculates on change
with 300ms debounce. `useSpotDate(pair, tradeDate, tenor)` skips API when any field empty.
Local history of last 5 calculations stored in component state.

## Files to Create

- `frontend/src/features/dates/SpotCalculatorPage.tsx`
- `frontend/src/features/dates/DateResult.tsx`
- `frontend/src/hooks/useSpotDate.ts`
- `frontend/src/features/dates/SpotCalculatorPage.test.tsx`

## Files to Modify

- `frontend/src/App.tsx` — add `/dates` route + nav link
