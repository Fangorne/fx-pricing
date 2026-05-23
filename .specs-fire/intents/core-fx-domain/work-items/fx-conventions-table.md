---
id: fx-conventions-table
title: FX Convention Registry
intent: core-fx-domain
complexity: medium
mode: confirm
status: completed
depends_on:
  - fx-spot-value-dates
created: 2026-05-22T00:00:00Z
run_id: run-fx-pricing-006
completed_at: 2026-05-23T10:37:06.457Z
---

# Work Item: FX Convention Registry

## Description

Implémenter `FXConvention` dataclass et le registry `FX_CONVENTIONS` avec toutes les paires G10 majeures. `FXConvention` encapsule : spot_lag, day_count_basis (Act/360, Act/365, Act/Act), roll_convention (ModifiedFollowing par défaut), pip_precision (nb de décimales), quotation_side. Fonction `get_convention(pair) → FXConvention`.

Fichiers cibles :
- `app/domain/conventions.py` — `FXConvention`, `DayCountBasis`, `FX_CONVENTIONS`, `get_convention()`
- `tests/unit/domain/test_conventions.py`

## Acceptance Criteria

- [ ] `get_convention("EUR/USD")` → spot_lag=2, day_count=Act/360, roll=ModifiedFollowing, pip_precision=4
- [ ] `get_convention("USD/JPY")` → spot_lag=2, pip_precision=2 (cotation à 2 décimales)
- [ ] `get_convention("USD/CAD")` → spot_lag=1, day_count=Act/365
- [ ] `get_convention("GBP/USD")` → spot_lag=2, day_count=Act/365, pip_precision=4
- [ ] `get_convention("EUR/JPY")` → pip_precision=2
- [ ] `get_convention("USD/CHF")` → spot_lag=2, day_count=Act/360
- [ ] `get_convention("AUD/USD")` → spot_lag=2, day_count=Act/365
- [ ] `get_convention("NZD/USD")` → spot_lag=2
- [ ] Paires couvertes : EURUSD, USDJPY, GBPUSD, USDCHF, USDCAD, AUDUSD, NZDUSD, EURGBP, EURJPY, EURCHF, GBPJPY, AUDJPY
- [ ] `get_convention("XXX/YYY")` non supportée → `UnsupportedCurrencyPairError`
- [ ] `DayCountBasis` enum : ACT_360, ACT_365, ACT_ACT

## Technical Notes

- `FXConvention` : `@dataclass(frozen=True)`
- `DayCountBasis` utilisé plus tard par le pricing engine pour `year_fraction()`
- `UnsupportedCurrencyPairError` défini dans `app/domain/exceptions.py`

## Dependencies

- fx-spot-value-dates
