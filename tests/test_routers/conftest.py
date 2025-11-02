import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

API_BASE_URL = "http://test"


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=API_BASE_URL
    ) as client:
        yield client
