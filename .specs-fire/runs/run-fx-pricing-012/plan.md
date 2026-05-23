# Plan — run-fx-pricing-012

## Work Item: frontend-conventions-page
**Mode**: confirm | **Complexity**: medium

---

## Approach

Build `/conventions` route with 3 components + 1 custom hook. React Router v6
handles routing. Filter state is local. Selected pair drives ConventionDetail
via URL param `/:pair`. Dark theme matches existing App.tsx.

## Files to Create

- `frontend/src/features/conventions/ConventionsPage.tsx`
- `frontend/src/features/conventions/ConventionsList.tsx`
- `frontend/src/features/conventions/ConventionDetail.tsx`
- `frontend/src/hooks/useConventions.ts`
- `frontend/src/features/conventions/ConventionsPage.test.tsx`

## Files to Modify

- `frontend/src/App.tsx` — add Router + nav + Routes
- `frontend/package.json` — add react-router-dom v6
