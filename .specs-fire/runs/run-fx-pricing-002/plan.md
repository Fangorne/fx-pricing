---
run: run-fx-pricing-002
work_item: fx-core-types
intent: core-fx-domain
mode: autopilot
generated: "2026-05-22T17:09:30Z"
---

# Plan: FX Core Value Objects

## Approach

Implement four pure domain value objects in `app/domain/types.py` using stdlib only:

1. `Currency` — `enum.StrEnum` with G10+ ISO 4217 codes
2. `CurrencyPair` — `@dataclass(frozen=True)` with parsing and validation
3. `Tenor` — `@dataclass(frozen=True)` with string parsing and approximate day conversion
4. `QuotationSide` — `enum.Enum` with DIRECT / INDIRECT

## Files to Create

| File | Purpose |
|------|---------|
| `backend/app/domain/types.py` | All four value objects |
| `backend/tests/unit/domain/__init__.py` | Test sub-package marker |
| `backend/tests/unit/domain/test_types.py` | 100% unit test coverage |

## Files to Modify

None.

## Tests

- `tests/unit/domain/test_types.py` — parametrized tests for all acceptance criteria
- Target: 100% coverage on `app/domain/types.py`
