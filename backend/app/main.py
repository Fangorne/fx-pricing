from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.prices import router as prices_router
from app.api.routers.reference import router as reference_router
from app.api.routers.ws_prices import router as ws_prices_router
from app.config import get_settings

settings = get_settings()

_DESCRIPTION = """
## FX Pricing Platform — Reference Data API

Institutional-grade reference data for **G10 FX markets**.

### Features

- **Conventions** — Spot lag, day count basis, roll convention, and pip precision for all G10 pairs
- **Calendars** — Holiday calendars for each G10 currency (FED, ECB, BOE, BOJ, SNB, BOC, RBA, RBNZ, RIX, NB)
- **Date Calculator** — Spot and value date generation respecting market conventions and business day rules

### Coverage

| | |
|---|---|
| Currency pairs | EUR/USD, USD/JPY, GBP/USD, USD/CHF, USD/CAD, AUD/USD, NZD/USD + crosses |
| Calendars | USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD, SEK, NOK |
| Tenors | ON, TN, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y |
"""

_TAGS = [
    {
        "name": "Conventions",
        "description": (
            "FX market conventions — spot lag, day count basis (Act/360, Act/365), "
            "roll convention (Modified Following), pip precision, and quotation side."
        ),
    },
    {
        "name": "Calendars",
        "description": (
            "Market holiday calendars for G10 currencies. "
            "Holidays are computed from official central bank schedules (FED, ECB, BOE, BOJ…). "
            "Use the business-day endpoint to check any date."
        ),
    },
    {
        "name": "Date Calculator",
        "description": (
            "Spot and value date generation. Applies spot lag, business day adjustment "
            "(Modified Following by default), and combined currency calendars."
        ),
    },
    {
        "name": "Prices",
        "description": (
            "Live FX spot prices via Yahoo Finance with Redis caching. "
            "Returns bid, ask, mid, and staleness metadata. "
            "Stale prices are served transparently when the provider is unavailable."
        ),
    },
    {
        "name": "Health",
        "description": "Service health check.",
    },
]

app = FastAPI(
    title="FX Pricing API",
    description=_DESCRIPTION,
    version="0.1.0",
    openapi_tags=_TAGS,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reference_router)
app.include_router(prices_router)
app.include_router(ws_prices_router)


@app.get("/health", tags=["Health"], summary="Health check")
async def health() -> dict[str, str]:
    """Returns `{"status": "ok"}` when the service is running."""
    return {"status": "ok"}
