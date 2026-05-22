 ---
id: fx-core-types
title: FX Core Value Objects
intent: core-fx-domain
complexity: low
mode: autopilot
status: pending
depends_on: [project-scaffold]
created: "2026-05-22T00:00:00Z"
---

# Work Item: FX Core Value Objects

## Description

Implémenter les value objects purs du domaine FX : `Currency` (enum ISO 4217 G10+), `CurrencyPair` (base/quote, validation, parsing), `Tenor` (ON, TN, SN, 1W, 2W, 1M…12M, 1Y, 2Y, parsing), `QuotationSide` enum (direct/indirect). Ces types sont la base de tout le domaine FX.

Fichiers cibles : `app/domain/types.py` + `tests/unit/domain/test_types.py`

## Acceptance Criteria

- [ ] `Currency` enum couvre au minimum : USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD, SEK, NOK, DKK
- [ ] `CurrencyPair("EUR", "USD")` → base=EUR, quote=USD, str="EUR/USD"
- [ ] `CurrencyPair.from_string("EURUSD")` et `CurrencyPair.from_string("EUR/USD")` fonctionnent
- [ ] `CurrencyPair` valide que base ≠ quote, lève `ValueError` sinon
- [ ] `Tenor.from_string("ON")`, `"1W"`, `"3M"`, `"1Y"` parsent correctement
- [ ] `Tenor` expose `to_days()` → entier approx (ON=1, 1W=7, 1M=30, 3M=91, 1Y=365)
- [ ] `QuotationSide.DIRECT` (1 unité base = X quote) et `INDIRECT` définis
- [ ] Tests unitaires : 100% couverture sur `app/domain/types.py`

## Technical Notes

- Utiliser `@dataclass(frozen=True)` pour l'immutabilité des value objects
- `Currency` : `enum.StrEnum` pour compatibilité string directe
- Pas de dépendance externe — stdlib uniquement

## Dependencies

- project-scaffold
