import pytest
from sqlalchemy import select

from app.models.user import User
from app.schemas.auth import AccessToken
from app.schemas.user import UserOut

from .conftest import assert_output_schema

AUTH_BASE_URL = "/auth"


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_user")
@pytest.mark.parametrize(
    "data,expected_status",
    [
        (
            {"name": "John Smith", "email": "john@gmail.com", "password": "teStPa331!"},
            200,
        ),
        (
            {
                "name": "  ",
                "email": "john@gmail.com",
                "password": "teStPa331!",
            },  # empty name
            422,
        ),
        (
            {
                "name": "John Smith",
                "email": "john@gmail.com",
                "password": "weakpassword",  # weak password
            },
            422,
        ),
        (
            {
                "name": "John Smith",
                "email": "invalidmail.com",  # invalid email
                "password": "teStPa331!",
            },
            422,
        ),
        (
            {
                "name": "John Smith",
                "email": "janesmith@gmail.com",  # existent user email
                "password": "teStPa331!",
            },
            400,
        ),
    ],
    ids=[
        "Valid sign up",
        "Empty name",
        "Weak password",
        "Invalid email",
        "Existent user with email",
    ],
)
async def test_auth_signup(async_client, db, data, expected_status):
    response = await async_client.post(f"{AUTH_BASE_URL}/signup", json=data)
    response_status_code = response.status_code
    assert response_status_code == expected_status
    if response_status_code == 200:
        assert_output_schema(data=response.json(), schema=UserOut)

        result = await db.execute(select(User).where(User.email == data.get("email")))
        db_record = result.scalar_one_or_none()
        assert db_record
        assert db_record.name == data["name"]
        assert db_record.hashed_password != data["password"]

        response_data = response.json()
        assert "id" in response_data


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_user")
@pytest.mark.parametrize(
    "data,expected_status",
    [
        ({"username": "janesmith@gmail.com", "password": "TestPassword123!"}, 200),
        (
            {"username": "janesmith@gmail.com", "password": "wrongpassword"},
            403,
        ),  # wrong password
        (
            {"username": "wrong@email.com", "password": "TestPassword123!"},
            403,
        ),  # wrong email
    ],
)
async def test_auth_login(async_client, data, expected_status):
    response = await async_client.post(
        f"{AUTH_BASE_URL}/login",
        data=data,
    )
    assert response.status_code == expected_status
    data = response.json()
    if response.status_code == 200:
        assert_output_schema(data=response.json(), schema=AccessToken)
    else:
        assert data["detail"] == "Incorrect username or password"
