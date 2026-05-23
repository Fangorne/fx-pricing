"""Pydantic v2 response schemas for the reference data API."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class ConventionResponse(BaseModel):
    pair: str
    spot_lag: int
    day_count: str
    roll_convention: str
    pip_precision: int
    quotation_side: str


class HolidayResponse(BaseModel):
    date: date
    name: str


class BusinessDayResponse(BaseModel):
    date: date
    currency: str
    is_business_day: bool
    reason: str | None = None


class SpotDateResponse(BaseModel):
    pair: str
    trade_date: date
    spot_date: date


class ValueDateResponse(BaseModel):
    pair: str
    trade_date: date
    tenor: str
    spot_date: date
    value_date: date
