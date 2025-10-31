import pytest

from app.models.user import User


@pytest.fixture(scope="function")
async def test_user(db):
    user_record = User(
        name="Jane Smith",
        email="janesmith@gmail.com",
    )
    db.add(user_record)
    await db.commit()
    await db.refresh(user_record)
    yield user_record
