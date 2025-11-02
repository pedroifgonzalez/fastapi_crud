import pytest

from app.models.user import User
from app.services.converters.passwords import PasswordConverter

pwd_converter = PasswordConverter()
PASSWORD_HASHED = pwd_converter.to_hash("TestPassword123!")


@pytest.fixture(scope="function")
async def test_user(db):
    user_record = User(
        name="Jane Smith",
        email="janesmith@gmail.com",
        hashed_password=PASSWORD_HASHED,
    )
    db.add(user_record)
    await db.commit()
    await db.refresh(user_record)
    yield user_record
