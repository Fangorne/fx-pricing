---
id: frontend-fx-reference
title: Frontend FX Conventions & Calendars
status: in_progress
created: "2026-05-22T00:00:00Z"
---

# Intent: Frontend FX Conventions & Calendars

## Goal

Application web frontend permettant de consulter et d'explorer les calendriers de marché et les conventions FX — interface utilisateur pour le domaine FX sans fonctionnalité de pricing dans un premier temps.

## Users

Traders, sales FX, et développeurs qui ont besoin de vérifier rapidement les conventions d'une paire, les jours fériés d'une devise, ou les dates spot/value.

## Problem

Les conventions FX et calendriers sont dans le code — inaccessibles sans passer par un développeur. Une interface web permet de les consulter, valider et partager facilement.

## Success Criteria

- Recherche et affichage des conventions d'une paire FX (spot lag, day count, pip precision, roll convention)
- Consultation du calendrier d'une devise : jours fériés par année, is_business_day pour une date donnée
- Calcul de date spot/value pour une paire et un ténor donnés
- Interface réactive, mise à jour sans reload
- Stack : React 18 + TypeScript + Tailwind CSS

## Constraints

- Consomme l'API backend FastAPI (dépend de core-fx-domain + backend API endpoints)
- Pas de pricing dans cet intent — conventions et calendriers uniquement
- Frontend standalone dans `frontend/` à la racine du projet

## Notes

Dépend de `fx-conventions-table` et `fx-market-calendar` (intent core-fx-domain) pour les données.
