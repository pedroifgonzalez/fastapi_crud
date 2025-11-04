import pytest

from app.core.security.roles import UserRole
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


@pytest.fixture(scope="function")
async def test_admin_user(db):
    admin_user_record = User(
        name="Admin",
        email="adminuser@gmail.com",
        hashed_password=PASSWORD_HASHED,
        role=UserRole.ADMIN.value,
    )
    db.add(admin_user_record)
    await db.commit()
    await db.refresh(admin_user_record)
    yield admin_user_record


@pytest.fixture(scope="function")
async def test_deleted_user(db):
    deleted_user_record = User(
        id=10,
        name="Deleted User",
        email="deleteduser@gmail.com",
        hashed_password=PASSWORD_HASHED,
        is_deleted=True,
    )
    db.add(deleted_user_record)
    await db.commit()
    await db.refresh(deleted_user_record)
    yield deleted_user_record


@pytest.fixture(scope="function")
async def test_user_2(db):
    user_2_record = User(
        name="Ethan Smith",
        email="ethansmith@gmail.com",
        hashed_password=PASSWORD_HASHED,
    )
    db.add(user_2_record)
    await db.commit()
    await db.refresh(user_2_record)
    yield user_2_record


@pytest.fixture(scope="function")
async def test_multiple_users(db):
    number_of_users = 30
    users = []
    for number in range(1, number_of_users):
        user = User(
            name=f"User {number}",
            email=f"user{number}@gmail.com",
            hashed_password=PASSWORD_HASHED,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        users.append(user)
    yield users
