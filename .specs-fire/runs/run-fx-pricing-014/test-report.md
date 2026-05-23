# Test Report — run-fx-pricing-014

## Summary

All 17 frontend tests pass. Build is clean. Lint + Prettier pass.

## Commands

```
cd frontend && pnpm build   # ✓ TypeScript clean, vite build ok
cd frontend && pnpm test    # ✓ 17/17 passed
cd frontend && pnpm lint    # ✓ ESLint + Prettier clean
```

## Test Results

| Suite | Tests | Status |
|-------|-------|--------|
| ConventionsPage.test.tsx | 5 | ✓ pass |
| CalendarPage.test.tsx | 6 | ✓ pass |
| SpotCalculatorPage.test.tsx | 6 | ✓ pass |
| **Total** | **17** | **✓ all pass** |

## SpotCalculatorPage Tests

- renders pair selector with all 12 pairs ✓
- renders tenor selector with 10 tenors ✓
- shows result after debounce with spot and value date ✓ (real timer, 1500ms waitFor)
- shows loading skeleton while fetching ✓
- shows error message on API failure ✓
- accumulates history entries ✓

## Fixes Applied During Testing

- Moved history accumulation from render body to `useEffect` to avoid setState-during-render
- Fixed `getByText(/Value Date/i)` collision with page title — switched to `getAllByText`
- Fixed loading skeleton `waitFor` — added explicit throw so `waitFor` retries
