from datetime import timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.security.tokens import TokenManager
from app.main import app

API_BASE_URL = "http://test"


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=API_BASE_URL
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def generate_test_token(test_user):
    token_manager = TokenManager(
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    token, _ = token_manager.generate_access_token(
        data={
            "sub": test_user.email,
            "exp": None,
        }
    )
    yield token
