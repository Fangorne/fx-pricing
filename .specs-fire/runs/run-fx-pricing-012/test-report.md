# Test Report — run-fx-pricing-012

## Work Item: frontend-conventions-page

### Test Results

| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| `ConventionsPage.test.tsx` (Vitest + Testing Library) | 5 | 0 | 0 |
| `pnpm build` (tsc + vite) | ✓ | — | — |
| `pnpm lint` (ESLint + Prettier) | ✓ | — | — |

### Acceptance Criteria Validation

| Criterion | Status | Notes |
|-----------|--------|-------|
| `/conventions` affiche toutes les paires G10 | ✓ | Tested: 3-pair mock, all rendered |
| Searchbox filtre en temps réel | ✓ | Tested: "EUR" → EUR/USD only |
| Clic paire → détail convention | ✓ | URL param `:pair` drives ConventionDetail |
| Détail: Spot Lag, Day Count, Roll Conv., Pip Precision | ✓ | All fields shown in ConventionDetail |
| État de chargement (skeleton) | ✓ | Tested: animate-pulse skeleton shown |
| Message erreur si API inaccessible | ✓ | Tested: "API inaccessible" shown |
| Paire invalide → "Convention non trouvée" | ✓ | useConventionDetail maps 404 error |
| Responsive desktop/tablet | ✓ | `lg:grid-cols-2` layout |
| "Aucune paire trouvée" quand filtre vide | ✓ | Tested: XXXYYY filter |
