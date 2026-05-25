"""Pydantic v2 response schemas for the reference data API."""

from __future__ import annotations

from datetime import date as Date

from pydantic import BaseModel, Field


class ConventionResponse(BaseModel):
    pair: str = Field(examples=["EUR/USD"])
    spot_lag: int = Field(examples=[2])
    day_count: str = Field(examples=["Act/360"])
    roll_convention: str = Field(examples=["MODIFIED_FOLLOWING"])
    pip_precision: int = Field(examples=[4])
    quotation_side: str = Field(examples=["direct"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "pair": "EUR/USD",
                    "spot_lag": 2,
                    "day_count": "Act/360",
                    "roll_convention": "MODIFIED_FOLLOWING",
                    "pip_precision": 4,
                    "quotation_side": "direct",
                }
            ]
        }
    }


class HolidayResponse(BaseModel):
    date: Date = Field(examples=["2026-07-03"])
    name: str = Field(examples=["USD holiday"])

    model_config = {
        "json_schema_extra": {
            "examples": [{"date": "2026-07-03", "name": "USD holiday"}]
        }
    }


class BusinessDayResponse(BaseModel):
    date: Date = Field(examples=["2026-05-26"])
    currency: str = Field(examples=["USD"])
    is_business_day: bool = Field(examples=[True])
    reason: str | None = Field(default=None, examples=[None])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "date": "2026-05-26",
                    "currency": "USD",
                    "is_business_day": True,
                    "reason": None,
                }
            ]
        }
    }


class SpotDateResponse(BaseModel):
    pair: str = Field(examples=["EUR/USD"])
    trade_date: Date = Field(examples=["2026-05-22"])
    spot_date: Date = Field(examples=["2026-05-27"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "pair": "EUR/USD",
                    "trade_date": "2026-05-22",
                    "spot_date": "2026-05-27",
                }
            ]
        }
    }


class ValueDateResponse(BaseModel):
    pair: str = Field(examples=["EUR/USD"])
    trade_date: Date = Field(examples=["2026-05-22"])
    tenor: str = Field(examples=["3M"])
    spot_date: Date = Field(examples=["2026-05-27"])
    value_date: Date = Field(examples=["2026-08-27"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "pair": "EUR/USD",
                    "trade_date": "2026-05-22",
                    "tenor": "3M",
                    "spot_date": "2026-05-27",
                    "value_date": "2026-08-27",
                }
            ]
        }
    }
