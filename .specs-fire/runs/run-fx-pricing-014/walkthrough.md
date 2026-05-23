# Walkthrough — run-fx-pricing-014

**Work Item**: frontend-spot-calculator  
**Intent**: frontend-fx-reference  
**Completed**: 2026-05-23

## What Was Built

Spot/Value Date calculator page at `/dates` route. Users select a currency pair, trade date, and tenor; the page fetches spot date, value date, and convention in parallel and displays results with a history of the last 5 calculations.

## Files Created

| File | Purpose |
|------|---------|
| `frontend/src/hooks/useSpotDate.ts` | Hook — parallel fetch with 300ms debounce, cancellation |
| `frontend/src/features/dates/DateResult.tsx` | Result card with Row sub-component |
| `frontend/src/features/dates/SpotCalculatorPage.tsx` | Route page — form, result, history |
| `frontend/src/features/dates/SpotCalculatorPage.test.tsx` | 6 Vitest tests |

## Files Modified

| File | Change |
|------|--------|
| `frontend/src/App.tsx` | Added SpotCalculatorPage import, `/dates` route, "Calculateur" nav link |

## Key Decisions

**`Promise.allSettled` for parallel fetches**: spot, value, and convention fetched in parallel. Convention failure is non-blocking — spot/value still render. Only spot failure surfaces as an error.

**`useEffect` for history**: initial draft called `setHistory` in the render body (setState-during-render). Moved to `useEffect([result])` with key-based deduplication to prevent double-entries.

**No extra debounce library**: same `useEffect + setTimeout(300) + clearTimeout` pattern as `useCalendar`.

## Deviations from Plan

None — all files match plan exactly.

## Tests (6)

- renders pair selector with all 12 pairs
- renders tenor selector with 10 tenors
- shows result after debounce with spot and value date
- shows loading skeleton while fetching
- shows error message on API failure
- accumulates history entries

## Developer Notes

- `/Value Date/i` matches the page title "Calculateur Spot / **Value Date**" — tests use `getAllByText` to handle multiple matches.
- `waitFor(() => element)` does not retry on null — callback must throw for retry. Used explicit `if (!el) throw new Error(...)`.
- History deduplication key: `pair|tradeDate|tenor` — prevents duplicate entry when result object reference changes but content is identical.
