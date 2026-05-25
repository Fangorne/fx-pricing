---
id: run-fx-pricing-017
scope: single
work_items:
  - id: db-repository-layer
    intent: database-swagger
    mode: confirm
    status: completed
current_item: db-repository-layer
status: completed
started: 2026-05-25T14:35:00.000Z
completed: 2026-05-25T14:50:00.000Z
---

# Run: run-fx-pricing-017

## Files Created
- `backend/app/infrastructure/repositories/__init__.py`
- `backend/app/infrastructure/repositories/convention_repository.py`
- `backend/app/infrastructure/repositories/calendar_repository.py`
- `backend/tests/unit/test_repositories.py`

## Decisions
- Used MagicMock (not __new__) for ORM model fixtures — SQLAlchemy descriptors block __new__ attribute assignment
- _DbBackedCalendar subclass holds holidays_by_year dict loaded from DB
