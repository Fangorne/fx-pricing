# System Architecture

## Overview

FX Pricing est une plateforme de pricing et de visualisation de produits FX vanilla (Spot, Forward, Swap, Option) en temps réel. Elle expose une API backend modulaire (REST + WebSocket) consommée par un frontend web interactif, avec abstraction complète des providers de market data.

## System Context

Les traders et sales FX utilisent le frontend pour pricer des produits, visualiser les market data en temps réel et gérer des tickets de booking. Le backend orchestre les calculs financiers, le streaming des prix et l'accès aux données de marché externes.

### Context Diagram

```
                    ┌─────────────────────────┐
                    │      FX Pricing          │
 ┌────────────┐     │  ┌─────────────────────┐ │     ┌──────────────────┐
 │   Trader   │────▶│  │  Frontend (React)   │ │     │  Yahoo Finance   │
 │   / Sales  │◀────│  │  Dashboard + Ticket │ │     │  (Market Data)   │
 └────────────┘     │  └────────┬────────────┘ │     └────────▲─────────┘
                    │           │ REST/WS       │              │
                    │  ┌────────▼────────────┐ │     ┌────────┴─────────┐
                    │  │  Backend (FastAPI)  │─┼────▶│  Bloomberg/      │
                    │  │  Pricing + Streaming│ │     │  Reuters (futur) │
                    │  └────────┬────────────┘ │     └──────────────────┘
                    │           │               │
                    │  ┌────────▼────────────┐ │
                    │  │  PostgreSQL + Redis  │ │
                    │  └─────────────────────┘ │
                    └─────────────────────────┘
```

### Users

- **Trader FX**: Pricing on-demand, suivi temps réel, booking de tickets FX
- **Sales FX**: Consultation prix, historique, configuration produits
- **Admin**: Gestion des calendriers, conventions, providers

### External Systems

- **Yahoo Finance**: Premier provider de market data (spots FX, taux indicatifs)
- **Bloomberg / Reuters**: Intégration future (données professionnelles)

## Architecture Pattern

**Pattern**: Clean Architecture (Domain-Driven) + Hexagonal (Ports & Adapters)
**Rationale**: Le domaine financier FX est riche et stable — la séparation stricte domaine/infrastructure permet de changer de provider market data sans toucher aux calculs. Le moteur de calcul stateless est testable isolément avec des valeurs de référence.

## Component Architecture

### Components

#### Domain Layer (`app/domain/`)

- **Purpose**: Règles métier FX pures, indépendantes de toute infrastructure
- **Responsibilities**: Conventions par paire, calculs pricing (Forward, B-S, Greeks), calendriers, validation métier
- **Dependencies**: Aucune dépendance externe — stdlib + numpy/scipy uniquement

#### Application Layer (`app/application/`)

- **Purpose**: Orchestration des use cases (pricer un Forward, streamer un spot, etc.)
- **Responsibilities**: Coordination domain + infrastructure, gestion staleness, cache strategy
- **Dependencies**: Domain layer + interfaces (Ports)

#### Infrastructure Layer (`app/infrastructure/`)

- **Purpose**: Implémentations concrètes des Ports définis dans le domaine
- **Responsibilities**: Provider Yahoo Finance, repos PostgreSQL, cache Redis, pub/sub WebSocket
- **Dependencies**: Application layer + librairies externes

#### API Layer (`app/api/`)

- **Purpose**: Exposition REST + WebSocket
- **Responsibilities**: Routing, auth JWT, mapping HTTP↔domaine, WebSocket session management
- **Dependencies**: Application layer

#### Frontend (`frontend/src/`)

- **Purpose**: Dashboard pricing et tickets FX interactifs
- **Responsibilities**: Streaming WebSocket, affichage temps réel, ticket FX, graphiques
- **Dependencies**: Backend API uniquement

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Backend                               │
│                                                          │
│  ┌──────────┐    ┌─────────────┐    ┌────────────────┐  │
│  │ API Layer│───▶│ Application │───▶│  Domain Layer  │  │
│  │ REST + WS│    │  Use Cases  │    │ FX Pure Logic  │  │
│  └──────────┘    └──────┬──────┘    └────────────────┘  │
│                         │                                │
│                  ┌──────▼──────────────────────────┐    │
│                  │       Infrastructure             │    │
│                  │  ┌──────────┐  ┌─────────────┐  │    │
│                  │  │ Yahoo FX │  │ PostgreSQL  │  │    │
│                  │  │ Provider │  │ Redis Cache │  │    │
│                  │  └──────────┘  └─────────────┘  │    │
│                  └─────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

**Pricing on-demand (REST)**: Client → API → Application (resolve conventions + fetch market data) → Domain (calcul pur) → Response

**Streaming temps réel (WebSocket)**: Client subscribe(pair) → WebSocket handler → Redis pub/sub → Market data update → Domain recalcul → push Client

```
REST Pricing:
  POST /pricing/forward
       │
       ▼
  Application Service
       │── fetch spot (Redis cache → Yahoo Finance si stale)
       │── fetch rates (Redis cache → Yahoo Finance si stale)
       │── resolve FXConvention(pair)
       │── resolve Calendar(pair)
       │
       ▼
  Domain: calculate_forward_rate(spot, r_d, r_f, days, convention)
       │
       ▼
  PricingResult → JSON response

WebSocket Streaming:
  WS subscribe("EURUSD")
       │
       ▼
  Redis SUBSCRIBE fx.prices.EURUSD
       │
  [Market data refresh loop]
       │── Yahoo Finance fetch → Redis publish
       │── Domain recalcul automatique
       ▼
  WS push PriceUpdate → Client
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Domain | Python + numpy/scipy | Calculs financiers purs (pricing, Greeks, interpolation) |
| Application | Python + FastAPI async | Orchestration use cases, gestion cache/staleness |
| API REST | FastAPI + Pydantic v2 | Endpoints pricing, auth, conventions, calendriers |
| API WebSocket | FastAPI WebSocket | Streaming temps réel, gestion subscriptions |
| Cache / Pub-Sub | Redis 7 | Market data cache TTL + diffusion événementielle |
| Persistence | PostgreSQL + SQLAlchemy | Historique, conventions, calendriers, sessions |
| Market Data | Yahoo Finance (yfinance) | Provider initial — spots FX, taux indicatifs |
| Frontend UI | React 18 + TypeScript | Dashboard, ticket FX, visualisation |
| Frontend State | Zustand | État global pricing + subscriptions WS |
| Frontend Charts | TradingView LW Charts | Graphiques OHLC FX |
| Frontend RT | WebSocket API natif | Streaming zero-polling |
| Containerisation | Docker + Compose | Environnement reproductible |
| CI/CD | GitHub Actions | Tests, lint, déploiement |

## Non-Functional Requirements

### Performance

- **Latence pricing REST**: < 100ms p99 (hors fetch provider)
- **Latence WebSocket push**: < 50ms p99 (post market data update)
- **Throughput**: 100 clients WebSocket simultanés (phase 1)
- **Cache hit rate**: > 95% sur les spots FX (TTL 5s)

### Security

- Authentification JWT (python-jose) — tous les endpoints pricing
- HTTPS obligatoire en production
- Rate limiting sur les endpoints de pricing
- Credentials providers stockés en variables d'environnement uniquement

### Scalability

Architecture stateless côté pricing : le moteur de calcul est une fonction pure, horizontalement scalable. Redis centralise l'état partagé (cache + pub/sub). Phase 2 : découplage microservices (pricing engine / market data service / API gateway).

## Constraints

- Premier provider Yahoo Finance uniquement (gratuit, sans clé) — données indicatives, non temps réel strict
- Précision numérique : float64 numpy pour les courbes, `Decimal` Python pour les notionals
- Pas de dépendance Bloomberg/Reuters en phase 1 (architecture provider abstraction prête)
- Timezone : toutes les dates internes en UTC, conversion au display

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | Clean/Hexagonal | Domaine FX stable, infrastructure changeante (providers) |
| Provider abstraction | Port/Adapter pattern | Yahoo Finance → Bloomberg sans toucher au pricing |
| Real-time | WebSocket + Redis pub/sub | Zero polling, faible latence, architecture événementielle |
| Calcul financier | numpy/scipy (pas QuantLib) | Suffisant pour vanilla FX, dépendance plus légère |
| Précision | float64 pour courbes, Decimal pour notionals | Balance précision/performance |
| État frontend | Zustand (pas Redux) | Léger, adapté aux flux de données haute fréquence |

---
*Generated by specs.md - fabriqa.ai FIRE Flow*
