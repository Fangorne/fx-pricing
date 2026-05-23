# Test Report — run-fx-pricing-013

## Work Item: frontend-calendar-page

### Test Results

| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| `CalendarPage.test.tsx` (6 tests) | 6 | 0 | 0 |
| `ConventionsPage.test.tsx` (5 tests, no regression) | 5 | 0 | 0 |
| `pnpm build` | ✓ | — | — |
| `pnpm lint` | ✓ | — | — |

### Acceptance Criteria Validation

| Criterion | Status | Notes |
|-----------|--------|-------|
| Route `/calendars` avec sélecteur devise | ✓ | 10 currencies tested |
| Sélection devise → liste jours fériés pour l'année | ✓ | `useCalendar(currency, year)` refetches |
| Sélecteur d'année (±2 ans) | ✓ | 5 options tested |
| Chaque jour férié avec date + nom | ✓ | `HolidayList` table |
| Section "Vérifier une date" avec badge vert/rouge | ✓ | `BusinessDayChecker` |
| Résultat mis à jour avec debounce 300ms | ✓ | Tested: 324ms real-timer test |
| Weekend détecté côté client sans appel API | ✓ | Tested: `checkBusinessDay` not called |
| État de chargement pendant fetch | ✓ | animate-pulse skeleton tested |
