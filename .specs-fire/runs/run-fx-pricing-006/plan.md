---
run: run-fx-pricing-006
work_item: fx-conventions-table
intent: core-fx-domain
mode: confirm
checkpoint: approved
generated: "2026-05-23T10:34:00Z"
---

# Plan: FX Convention Registry

## Files to Create

| File | Purpose |
|------|---------|
| `backend/app/domain/exceptions.py` | `FXDomainError`, `UnsupportedCurrencyPairError` |
| `backend/app/domain/conventions.py` | `DayCountBasis`, `FXConvention`, `FX_CONVENTIONS`, `get_convention()` |
| `backend/tests/unit/domain/test_conventions.py` | All acceptance criteria |

## G10 Registry (12 pairs)

EUR/USD·2·Act360·4·Direct | USD/JPY·2·Act360·2·Indirect | GBP/USD·2·Act365·4·Direct
USD/CHF·2·Act360·4·Indirect | USD/CAD·1·Act365·4·Indirect | AUD/USD·2·Act365·4·Direct
NZD/USD·2·Act365·4·Direct | EUR/GBP·2·Act360·4·Direct | EUR/JPY·2·Act360·2·Direct
EUR/CHF·2·Act360·4·Direct | GBP/JPY·2·Act365·2·Direct | AUD/JPY·2·Act365·2·Direct
