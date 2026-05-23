"""Integration tests for the /api/v1 reference data endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_conventions_returns_all(client: AsyncClient) -> None:
    response = await client.get("/api/v1/conventions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 12  # at least the G10 pairs in the registry
    pairs = {item["pair"] for item in data}
    assert "EUR/USD" in pairs
    assert "USD/JPY" in pairs


@pytest.mark.asyncio
async def test_get_convention_slash_format(client: AsyncClient) -> None:
    response = await client.get("/api/v1/conventions/EUR/USD")
    assert response.status_code == 200
    data = response.json()
    assert data["pair"] == "EUR/USD"
    assert data["spot_lag"] == 2
    assert data["pip_precision"] == 4


@pytest.mark.asyncio
async def test_get_convention_no_slash_format(client: AsyncClient) -> None:
    response = await client.get("/api/v1/conventions/EURUSD")
    assert response.status_code == 200
    data = response.json()
    assert data["spot_lag"] == 2


@pytest.mark.asyncio
async def test_get_convention_unknown_pair_returns_404(client: AsyncClient) -> None:
    response = await client.get("/api/v1/conventions/XXXYYY")
    assert response.status_code == 404
    assert "convention" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_holidays_usd_2026(client: AsyncClient) -> None:
    response = await client.get("/api/v1/calendars/USD/holidays?year=2026")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    dates = {item["date"] for item in data}
    assert "2026-07-04" not in dates  # Independence Day on Saturday → observed Friday Jul 3
    assert "2026-07-03" in dates


@pytest.mark.asyncio
async def test_get_holidays_unknown_currency_returns_404(client: AsyncClient) -> None:
    response = await client.get("/api/v1/calendars/XYZ/holidays?year=2026")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_business_day_true(client: AsyncClient) -> None:
    # 2026-05-26 is Tuesday — a business day for USD
    response = await client.get("/api/v1/calendars/USD/business-day?date=2026-05-26")
    assert response.status_code == 200
    data = response.json()
    assert data["is_business_day"] is True
    assert data["currency"] == "USD"
    assert data["reason"] is None


@pytest.mark.asyncio
async def test_business_day_weekend(client: AsyncClient) -> None:
    # 2026-05-23 is Saturday
    response = await client.get("/api/v1/calendars/USD/business-day?date=2026-05-23")
    assert response.status_code == 200
    data = response.json()
    assert data["is_business_day"] is False
    assert data["reason"] == "Weekend"


@pytest.mark.asyncio
async def test_business_day_holiday(client: AsyncClient) -> None:
    # 2026-12-25 is Christmas — a holiday for USD (observed on Friday Dec 25 since it's a Friday)
    response = await client.get("/api/v1/calendars/USD/business-day?date=2026-12-25")
    assert response.status_code == 200
    data = response.json()
    assert data["is_business_day"] is False


@pytest.mark.asyncio
async def test_spot_date_eurusd(client: AsyncClient) -> None:
    # 2026-05-22 is Friday. May 25 is Memorial Day (last Mon May).
    # +1 BD = Tue May 26, +2 BD = Wed May 27 → spot = 2026-05-27
    response = await client.get("/api/v1/spot-dates?pair=EUR/USD&trade_date=2026-05-22")
    assert response.status_code == 200
    data = response.json()
    assert data["spot_date"] == "2026-05-27"
    assert data["pair"] == "EUR/USD"


@pytest.mark.asyncio
async def test_value_date_eurusd_3m(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/spot-dates/value?pair=EUR/USD&trade_date=2026-05-22&tenor=3M"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tenor"] == "3M"
    assert "value_date" in data
    assert "spot_date" in data


@pytest.mark.asyncio
async def test_spot_date_unknown_pair_returns_404(client: AsyncClient) -> None:
    response = await client.get("/api/v1/spot-dates?pair=XXXYYY&trade_date=2026-05-22")
    # XXXYYY parses as an unknown Currency → 422 from CurrencyPair.from_string
    assert response.status_code in (404, 422)


@pytest.mark.asyncio
async def test_value_date_invalid_tenor(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/spot-dates/value?pair=EUR/USD&trade_date=2026-05-22&tenor=BADTENOR"
    )
    assert response.status_code == 422
