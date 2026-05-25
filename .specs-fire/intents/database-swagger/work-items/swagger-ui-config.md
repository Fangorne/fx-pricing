---
id: swagger-ui-config
title: Configuration Swagger UI
intent: database-swagger
complexity: low
mode: autopilot
status: pending
depends_on: [db-wire-api]
created: 2026-05-25T12:00:00Z
---

# Work Item: Swagger UI Configuration

## Description

Configurer FastAPI pour exposer une page Swagger UI professionnelle : tags par domaine, descriptions des endpoints, exemples de réponse, métadonnées de l'API. Ajouter aussi ReDoc comme alternative.

## Acceptance Criteria

- [ ] `app/main.py` configure `FastAPI(title, description, version, openapi_tags)`
- [ ] Tags définis : `Conventions`, `Calendars`, `Date Calculator`
- [ ] Chaque endpoint a `summary`, `description`, et `response_description`
- [ ] Les schémas Pydantic ont des `examples` (via `model_config` ou `Field(examples=[...])`)
- [ ] `/docs` (Swagger UI) et `/redoc` (ReDoc) accessibles
- [ ] `/openapi.json` retourne le schéma complet valide OpenAPI 3.1

## Technical Notes

- `openapi_tags` dans le constructeur FastAPI pour la navigation par section
- `responses={404: {"description": "Pair not found"}}` sur les endpoints concernés
- Utiliser `Field(examples=[...])` Pydantic v2 (pas `example=` déprécié)

## Dependencies

- db-wire-api
