"""Market data router — live FX spot prices."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_price_cache, get_provider
from app.api.schemas.prices import SpotPriceResponse
from app.domain.conventions import FX_CONVENTIONS
from app.domain.exceptions import MarketDataUnavailableError
from app.domain.market_data import SpotPrice
from app.infrastructure.cache.price_cache import PriceCache
from app.infrastructure.providers.base import MarketDataProvider

router = APIRouter(prefix="/api/v1", tags=["Prices"])

_G10_PAIRS = list(FX_CONVENTIONS.keys())

_503 = {503: {"description": "Market data provider unavailable and cache is empty"}}
_404 = {404: {"description": "Currency pair not supported"}}


def _to_response(price: SpotPrice, stale_threshold: int = 60) -> SpotPriceResponse:
    now = datetime.now(tz=timezone.utc)
    age = (now - price.timestamp).total_seconds()
    return SpotPriceResponse(
        pair=price.pair,
        bid=price.bid,
        ask=price.ask,
        mid=price.mid,
        timestamp=price.timestamp,
        is_stale=price.is_stale(stale_threshold),
        age_seconds=round(age, 1),
    )


@router.get(
    "/prices/{pair:path}",
    response_model=SpotPriceResponse,
    summary="Get spot price for a currency pair",
    description=(
        "Returns the latest FX spot price for a single G10 currency pair. "
        "Data is served from the Redis cache when fresh; otherwise fetched live from Yahoo Finance."
        "If the provider is unavailable but a stale cached value exists, it is returned with `is_stale=true`."
    ),
    response_description="Live or cached spot price with staleness metadata",
    responses={
        404: {"description": "Currency pair not supported"},
        **_503,
    },
)
async def get_spot_price(
    pair: str,
    cache: Annotated[PriceCache, Depends(get_price_cache)],
    provider: Annotated[MarketDataProvider, Depends(get_provider)],
) -> SpotPriceResponse:
    pair = pair.upper().replace("-", "/")
    if pair not in FX_CONVENTIONS:
        raise HTTPException(
            status_code=404, detail=f"Currency pair {pair!r} is not a supported G10 pair"
        )
    try:
        price = await cache.get_or_fetch(pair, provider)
        return _to_response(price)
    except MarketDataUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get(
    "/prices",
    response_model=list[SpotPriceResponse],
    summary="Get spot prices for multiple pairs",
    description=(
        "Returns spot prices for all G10 pairs by default. "
        "Optionally filter with `?pairs=EUR/USD,USD/JPY`. "
        "Pairs that fail individually are omitted from the response rather than failing the whole request."
    ),
    response_description="List of spot prices",
    responses=_404,
)
async def get_spot_prices(
    cache: Annotated[PriceCache, Depends(get_price_cache)],
    provider: Annotated[MarketDataProvider, Depends(get_provider)],
    pairs: Annotated[
        str | None, Query(description="Comma-separated currency pairs, e.g. EUR/USD,USD/JPY")
    ] = None,
) -> list[SpotPriceResponse]:
    if pairs:
        requested = [p.strip().upper().replace("-", "/") for p in pairs.split(",")]
        unknown = [p for p in requested if p not in FX_CONVENTIONS]
        if unknown:
            raise HTTPException(status_code=404, detail=f"Unsupported pairs: {', '.join(unknown)}")
        target_pairs = requested
    else:
        target_pairs = _G10_PAIRS

    results: list[SpotPriceResponse] = []
    for pair in target_pairs:
        try:
            price = await cache.get_or_fetch(pair, provider)
            results.append(_to_response(price))
        except MarketDataUnavailableError:
            pass  # silently omit failed pairs in bulk fetch

    return results
