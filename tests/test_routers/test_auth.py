import pytest
from sqlalchemy import select

from app.models.user import User

AUTH_BASE_URL = "/auth"


@pytest.mark.asyncio
async def test_auth_signup(async_client, db):
    data = {"name": "John Smith", "email": "john@gmail.com", "password": "teStPa331!"}
    await async_client.post(f"{AUTH_BASE_URL}/signup", json=data)
    result = await db.execute(select(User).where(User.email == data.get("email")))
    db_record = result.scalar_one_or_none()
    assert db_record
    assert db_record.name == "John Smith"
    assert db_record.hashed_password != "teStPa331!"
