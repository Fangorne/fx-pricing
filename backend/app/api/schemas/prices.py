"""Pydantic schemas for market data / prices endpoints."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SpotPriceResponse(BaseModel):
    pair: str = Field(examples=["EUR/USD"])
    bid: float = Field(examples=[1.0850])
    ask: float = Field(examples=[1.0852])
    mid: float = Field(examples=[1.0851])
    timestamp: datetime = Field(examples=["2026-05-25T15:30:00Z"])
    is_stale: bool = Field(examples=[False])
    age_seconds: float = Field(examples=[3.7])

    model_config = {
        "json_schema_extra": {
            "example": {
                "pair": "EUR/USD",
                "bid": 1.0850,
                "ask": 1.0852,
                "mid": 1.0851,
                "timestamp": "2026-05-25T15:30:00Z",
                "is_stale": False,
                "age_seconds": 3.7,
            }
        }
    }
