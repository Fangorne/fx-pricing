---
id: core-fx-domain
title: Core FX Domain Layer
status: completed
created: 2026-05-22T00:00:00Z
completed_at: 2026-05-23T10:37:06.464Z
---

# Intent: Core FX Domain Layer

## Goal

Implement the pure FX domain layer — conventions, calendriers de marché, et validation — sans aucune dépendance infrastructure. Ces fondations sont requises par tous les autres modules (pricing engine, market data, API).

## Users

Developers building on top of the FX Pricing platform (internal); indirectly, traders and sales using the pricing engine.

## Problem

Sans un domaine FX propre et testé, toute la logique de pricing serait couplée à l'infrastructure. Les règles de marché (spot lag, calendriers, conventions par paire) doivent être exprimées explicitement pour garantir la précision financière et la testabilité.

## Success Criteria

- Toutes les paires G10 standard ont leurs conventions définies (spot lag, day count, quotation side, pip precision)
- Les calendriers de marché G10 couvrent les jours fériés officiels (Fed, ECB TARGET, BOJ, BOE, SNB, etc.)
- La génération de dates spot/value est correcte pour toutes les paires G10, validée par rapport à des dates de référence
- Les règles de business day adjustment (Following, Modified Following, Preceding) produisent des résultats corrects
- Couverture de tests ≥ 90% sur le domaine, 0 régression sur les valeurs de référence
- Aucune dépendance externe dans `app/domain/` (stdlib + numpy/scipy uniquement)

## Constraints

- Python 3.12, uv package manager
- Domaine pur : pas de FastAPI, pas de SQLAlchemy, pas de Redis dans cette couche
- Les calculs utilisent `float64` numpy pour les courbes, `Decimal` Python pour les notionals

## Notes

Premier intent du projet. Constitue le socle de toute la plateforme FX Pricing.
