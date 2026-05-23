# Plan — run-fx-pricing-013

## Work Item: frontend-calendar-page
**Mode**: confirm | **Complexity**: medium

---

## Approach

Build `/calendars` route: currency selector + year picker + holiday list + business day checker.
`useCalendar(currency, year)` refetches on either change. Weekend detection is client-side.
Debounce 300ms via `useEffect + setTimeout` — no extra library.

## Files to Create

- `frontend/src/features/calendars/CalendarPage.tsx`
- `frontend/src/features/calendars/HolidayList.tsx`
- `frontend/src/features/calendars/BusinessDayChecker.tsx`
- `frontend/src/hooks/useCalendar.ts`
- `frontend/src/features/calendars/CalendarPage.test.tsx`

## Files to Modify

- `frontend/src/App.tsx` — add `/calendars` route + nav link
