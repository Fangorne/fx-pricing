---
run: run-fx-pricing-012
work_item: frontend-conventions-page
intent: frontend-fx-reference
generated: 2026-05-23T11:42:25.283Z
mode: confirm
---

# Implementation Walkthrough: Page Conventions FX

## Summary

The `/conventions` route was implemented as a searchable list + detail panel using React Router v6, three focused components, and two custom hooks. The page fetches all G10 conventions from the backend on mount, filters them client-side via a search box, and shows the full convention detail in a side panel when a pair is selected via URL parameter.

## Structure Overview

```text
App (BrowserRouter)
  └── /conventions → ConventionsPage
        ├── useConventions() — fetches all pairs, manages loading/error
        ├── ConventionsList — renders filtered table with Link per row
        └── /conventions/:pair → ConventionDetail
              └── useConventionDetail(pair) — fetches single pair detail
```

Data flows one way: hooks fetch → components render. No global state. URL param drives which detail is shown, making the URL shareable.

## Files Changed

### Created

| File | Purpose |
|------|---------|
| `frontend/src/features/conventions/ConventionsPage.tsx` | Route page: search input, loading/error states, grid layout |
| `frontend/src/features/conventions/ConventionsList.tsx` | Table of filtered pairs, each row links to `/:pair` |
| `frontend/src/features/conventions/ConventionDetail.tsx` | Side panel with all 5 convention fields + skeleton loader |
| `frontend/src/hooks/useConventions.ts` | `useConventions()` and `useConventionDetail(pair)` hooks |
| `frontend/src/features/conventions/ConventionsPage.test.tsx` | 5 component tests (render, filter, loading, error, empty) |

### Modified

| File | Changes |
|------|---------|
| `frontend/src/App.tsx` | Wrapped in `BrowserRouter`, added `<Routes>` with `/` and `/conventions/:pair?` routes, nav header link |
| `frontend/src/services/api.ts` | Added `RawConvention` interface + `mapConvention()` to convert snake_case API response to camelCase; split `calculateSpotDate` / `calculateValueDate` into separate functions |
| `frontend/src/types/fx.ts` | Aligned `DayCountConvention` values to match backend (`Act/360` not `ACT/360`); aligned `BusinessDayConvention` to uppercase ISDA values; added `SpotDateResult` snake_case fields |
| `frontend/package.json` | Added `react-router-dom@6` dependency |

## Key Implementation Details

### 1. Snake_case → camelCase API Mapping

The backend returns `spot_lag`, `day_count`, `roll_convention`, `pip_precision`. A `mapConvention()` function in `api.ts` converts these to camelCase before they reach components. This keeps the type boundary clean — components only see `FXConvention`.

### 2. Cancellation Flag in Hooks

Both hooks use a `cancelled` boolean flag to prevent state updates after component unmount. This avoids the "Can't perform a React state update on an unmounted component" warning during fast navigation.

### 3. URL-Driven Detail Panel

Selecting a pair navigates to `/conventions/EUR%2FUSD` (encoded). `ConventionsPage` reads `useParams()` and passes the decoded pair to `ConventionDetail`. This makes the selected pair bookmarkable and back-button friendly.

### 4. Search Filter Logic

The filter normalises both query and pair to uppercase and removes slashes before comparing: `"EUR"` matches `"EUR/USD"` and `"EUR/GBP"` but not `"USD/JPY"`. This matches the acceptance criterion example exactly.

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| No Zustand | Local state only | Work item explicitly states "état local suffisant" |
| URL param for selected pair | `/conventions/:pair` | Makes selection shareable/bookmarkable; no prop drilling |
| `encodeURIComponent` on pair | Yes | `EUR/USD` must be encoded in URL; backend `{pair:path}` decodes it |
| Separate `useConventionDetail` | Own hook | Pair changes independently trigger separate fetch |

## Deviations from Plan

| Deviation | Reason |
|-----------|--------|
| `types/fx.ts` values updated | Backend sends `Act/360` (not `ACT/360`) and `MODIFIED_FOLLOWING` (not `ModifiedFollowing`) — types aligned to actual API contract |
| `calculateSpotDate` signature changed | Split from optional `tenor` to two separate functions matching the two backend endpoints |

## Dependencies Added

| Package | Why Needed |
|---------|------------|
| `react-router-dom@6` | Client-side routing for `/conventions` and `/conventions/:pair` |

## How to Verify

1. **Start backend + frontend**

   ```bash
   cd backend && uvicorn app.main:app --reload
   cd frontend && pnpm dev
   ```

2. **Navigate to conventions**

   Open http://localhost:3000/conventions — all G10 pairs listed.

3. **Search filter**

   Type `EUR` in the search box — only EUR pairs remain.

4. **Select a pair**

   Click `EUR/USD` — detail panel appears on the right with Spot Lag, Day Count, etc.

5. **Direct URL**

   Open http://localhost:3000/conventions/EUR%2FUSD — detail panel opens directly.

6. **Run tests**

   ```bash
   cd frontend && pnpm test
   # → 5 passed
   ```

## Test Coverage

- Tests added: 5
- Status: all passing
- Scenarios: list render, search filter, loading state, API error, empty filter result

## Ready for Review

- [x] All acceptance criteria met
- [x] Tests passing (5 new)
- [x] Build + lint clean
- [x] Developer notes captured

## Developer Notes

- **`encodeURIComponent` for pairs with slashes**: `EUR/USD` must be encoded as `EUR%2FUSD` in the URL. The backend's `{pair:path}` converter handles the slash; the frontend `encodeURIComponent` prevents the router from splitting it.
- **React Router v7 warnings**: Two future-flag warnings appear in tests (`v7_startTransition`, `v7_relativeSplatPath`). These are informational — add the flags to `<BrowserRouter future={{...}}>` before upgrading to v7.
- **Type alignment**: Always verify `DayCountConvention` and `BusinessDayConvention` values against the actual backend enum `.value` strings, not the enum member names.

---
*Generated by specs.md - fabriqa.ai FIRE Flow Run run-fx-pricing-012*
