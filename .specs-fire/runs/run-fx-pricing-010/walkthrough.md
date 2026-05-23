---
run: run-fx-pricing-010
work_item: frontend-scaffold
intent: frontend-fx-reference
generated: 2026-05-23T11:30:00.000Z
mode: autopilot
---

# Implementation Walkthrough: Frontend Scaffold (Vite + React + TypeScript + Tailwind)

## Summary

A complete frontend project scaffold was created in `frontend/` using Vite 5, React 18, TypeScript (strict), and Tailwind CSS 3. The scaffold includes the FX domain type definitions, an HTTP API client wired to the FastAPI backend, and is integrated into `docker-compose.yml` as a hot-reloading dev container on port 3000.

## Structure Overview

The frontend follows a feature-oriented layout. The `types/` layer defines the FX domain model shared with the backend. The `services/` layer provides typed fetch wrappers for each backend API endpoint. The `components/`, `features/`, and `hooks/` directories are empty stubs ready for subsequent work items. The build pipeline (Vite) handles path aliasing (`@/` → `src/`), TypeScript compilation, and Tailwind CSS purging.

## Files Changed

### Created

| File | Purpose |
|------|---------|
| `frontend/package.json` | pnpm project manifest with all deps and scripts |
| `frontend/index.html` | Vite HTML entry point |
| `frontend/vite.config.ts` | Vite + Vitest config with `@/` path alias |
| `frontend/tsconfig.json` | TypeScript project references root |
| `frontend/tsconfig.app.json` | App TS config (strict, vite/client types, `@/*` paths) |
| `frontend/tsconfig.node.json` | Node TS config for vite.config.ts |
| `frontend/tailwind.config.js` | Tailwind CSS content scanning config |
| `frontend/postcss.config.js` | PostCSS with tailwindcss + autoprefixer |
| `frontend/eslint.config.js` | ESLint 9 flat config (TypeScript + React Hooks) |
| `frontend/.prettierrc` | Prettier formatting config |
| `frontend/.env.local` | `VITE_API_BASE_URL=http://localhost:8000` |
| `frontend/src/main.tsx` | React 18 root entry (`createRoot`) |
| `frontend/src/App.tsx` | Root component with Tailwind class |
| `frontend/src/index.css` | Tailwind `@tailwind` directives |
| `frontend/src/types/fx.ts` | FX domain types: `FXConvention`, `Currency`, `CurrencyPair`, `CalendarHoliday`, `SpotDateResult`, `BusinessDayCheckResult` |
| `frontend/src/services/api.ts` | Typed fetch client: `fetchConventions`, `fetchConvention`, `fetchHolidays`, `checkBusinessDay`, `calculateSpotDate` |
| `frontend/.npmrc` | pnpm esbuild build script allowance |
| `frontend/pnpm-workspace.yaml` | `allowBuilds: esbuild: true` |

### Modified

| File | Changes |
|------|---------|
| `docker-compose.yml` | Added `frontend` service: node:20-alpine, port 3000, volume mount, `pnpm dev` command |

## Domain Model

### TypeScript Types (frontend/src/types/fx.ts)

| Type | Properties | Notes |
|------|------------|-------|
| `Currency` | `string` alias | ISO 4217 code |
| `CurrencyPair` | `base`, `quote`, `symbol` | e.g. `{ base: "EUR", quote: "USD", symbol: "EURUSD" }` |
| `FXConvention` | `pair`, `spotLag`, `settlementCalendars`, `dayCount`, `businessDayConvention`, `pricingPrecision`, `pipSize` | Full market convention |
| `CalendarHoliday` | `date`, `currency`, `name`, `type` | Bank/settlement/both |
| `MarketCalendar` | `currency`, `year`, `holidays[]` | Calendar aggregate |
| `SpotDateResult` | `pair`, `tradeDate`, `spotDate`, `tenor`, `valueDate`, `businessDaysToSpot`, `calendarsApplied` | Spot/value date calculation result |
| `BusinessDayCheckResult` | `date`, `currency`, `isBusinessDay`, `reason?` | Business day validation result |

## Key Implementation Details

### 1. Vite Config: ESM-Compatible Path Alias

Used `fileURLToPath(new URL('./src', import.meta.url))` instead of `path.resolve(__dirname, './src')` to avoid needing `@types/node` for the alias and be compatible with ESM module resolution. `@types/node` was still added for `node:url` types.

### 2. Vitest Integration in Vite Config

Imported `defineConfig` from `vitest/config` (not `vite`) so the `test` block is type-safe without a separate `vitest.config.ts`.

### 3. API Client Pattern

All API functions share a single `get<T>()` helper that throws on non-2xx responses. This keeps each public function a one-liner while propagating errors correctly to callers.

### 4. pnpm esbuild Build Approval

pnpm 11 requires explicit approval for packages that run postinstall scripts. This is configured via `pnpm-workspace.yaml` (`allowBuilds: esbuild: true`) and `package.json` (`pnpm.allowedBuildScripts: ["esbuild"]`). Both are needed to satisfy different pnpm resolution paths.

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Vitest config location | Embedded in `vite.config.ts` | Avoids a separate config file; `vitest/config` provides types |
| No test setup file | Removed `setupFiles` reference | No tests yet; avoids broken import at scaffold stage |
| `--passWithNoTests` flag | Added to `pnpm test` script | Vitest exits 1 with no test files; scaffold phase has no tests |
| `BusinessDayCheckResult` type | Added beyond AC | Required by `checkBusinessDay()` return type; no cost to add |

## Deviations from Plan

| Deviation | Reason |
|-----------|--------|
| Added `frontend/.npmrc` and `pnpm-workspace.yaml` | pnpm 11 requires explicit `allowBuilds` approval for esbuild postinstall; not needed in earlier pnpm versions |
| Added `@eslint/js` and `@types/node` dev deps | Required by ESLint 9 flat config and `node:url` in vite.config.ts; not listed in original plan but standard for this stack |
| Removed `src/test-setup.ts` from vitest `setupFiles` | No setup file was created (scaffold only); referencing a non-existent file causes import errors |

## Dependencies Added

| Package | Why Needed |
|---------|------------|
| `@eslint/js` | ESLint 9 flat config base rules (peer dep not auto-installed) |
| `@types/node` | `node:url` types for `fileURLToPath` in `vite.config.ts` |

## How to Verify

1. **Install and start dev server**

   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

   Expected: Server starts at http://localhost:3000 with hot-reload.

2. **TypeScript build**

   ```bash
   pnpm build
   ```

   Expected: Clean build, output in `dist/`, no TypeScript errors.

3. **Lint**

   ```bash
   pnpm lint
   ```

   Expected: ESLint + Prettier both pass with no warnings.

4. **Tests**

   ```bash
   pnpm test
   ```

   Expected: `No test files found, exiting with code 0`.

5. **Docker Compose**

   ```bash
   docker compose up frontend
   ```

   Expected: Container starts, installs pnpm, runs `pnpm dev` on port 3000.

6. **Check Tailwind**

   Open http://localhost:3000 — the App component renders with `bg-blue-500` class applied.

## Test Coverage

- Tests added: 0
- Coverage: N/A
- Status: Scaffold only — no business logic to test

## Ready for Review

- [x] All acceptance criteria met
- [x] Tests passing (`--passWithNoTests`)
- [x] No critical issues
- [x] Developer notes captured

## Developer Notes

- **pnpm 11 esbuild**: `pnpm approve-builds` is interactive and can't run in CI. Use `pnpm-workspace.yaml` with `allowBuilds: esbuild: true` instead.
- **`vitest/config` vs `vite`**: Always import `defineConfig` from `vitest/config` when the config includes a `test` block, otherwise TypeScript errors on the `test` property.
- **Path alias `@/`**: Both `vite.config.ts` (runtime) and `tsconfig.app.json` (type checking) need the alias — they don't share config.
- **Docker volume**: The anonymous `/app/node_modules` volume in `docker-compose.yml` prevents the host's Windows `node_modules` from leaking into the Linux container.

---
*Generated by specs.md - fabriqa.ai FIRE Flow Run run-fx-pricing-010*
