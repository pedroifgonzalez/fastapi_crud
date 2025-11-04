import pytest

from app.schemas.user import UserOut
from app.utils.pagination import PaginatedResponse

from .conftest import assert_output_schema

USERS_BASE_URL = "/users"


@pytest.mark.asyncio
async def test_users_router_find_all(
    async_client, test_user, generate_admin_test_token
):
    response = await async_client.get(
        f"{USERS_BASE_URL}/",
        headers={"Authorization": f"Bearer {generate_admin_test_token}"},
    )
    data = response.json()
    assert data.get("total") > 0
    assert_output_schema(data=data, schema=PaginatedResponse[UserOut])


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_user", "test_deleted_user")
@pytest.mark.parametrize(
    "user_id,expected_status",
    [
        (1, 200),
        (10, 200),  # deleted user (allow it)
        (999, 404),  # non-existent user
    ],
)
async def test_users_router_find_one(
    async_client, user_id, expected_status, generate_admin_test_token
):
    response = await async_client.get(
        f"{USERS_BASE_URL}/{user_id}",
        headers={"Authorization": f"Bearer {generate_admin_test_token}"},
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert_output_schema(data=data, schema=UserOut)


@pytest.mark.usefixtures("test_user", "test_tag")
@pytest.mark.parametrize(
    "data,expected_status",
    [
        (
            {
                "name": "Frank Smith",
                "email": "franksmith@gmail.com",
                "password": "TestPassword123!",
            },
            200,
        ),
        (
            {
                "name": "  ",
                "email": "franksmith@gmail.com",
                "password": "TestPassword123!",
            },
            422,
        ),
        (
            {
                "name": "Frank Smith",
                "email": "franksmith@gmail.com",
                "password": "weakpassword",
            },
            422,
        ),
    ],
    ids=["Valid user", "Empty name", "Weak password"],
)
async def test_users_router_create(
    async_client, data, expected_status, generate_admin_test_token
):
    response = await async_client.post(
        f"{USERS_BASE_URL}/",
        json=data,
        headers={"Authorization": f"Bearer {generate_admin_test_token}"},
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert_output_schema(data=data, schema=UserOut)


@pytest.mark.usefixtures("test_user", "test_user_2", "test_tag")
@pytest.mark.parametrize(
    "user_id,data,expected_status",
    [
        (
            1,
            {"password": "N3wPa33!34"},
            200,
        ),
    ],
    ids=[
        "Update password",
    ],
)
async def test_users_router_update(
    async_client, user_id, data, expected_status, generate_admin_test_token
):
    response = await async_client.put(
        f"{USERS_BASE_URL}/{user_id}",
        json=data,
        headers={"Authorization": f"Bearer {generate_admin_test_token}"},
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert_output_schema(data=data, schema=UserOut)


@pytest.mark.usefixtures("test_user", "test_deleted_user", "test_user_2")
@pytest.mark.parametrize(
    "user_id,expected_status",
    [
        (1, 200),
        (10, 200),  # already deleted (silenced managed response)
        (999, 404),  # non-existent user
    ],
)
async def test_users_router_delete(
    async_client, user_id, expected_status, generate_admin_test_token
):
    response = await async_client.delete(
        f"{USERS_BASE_URL}/{user_id}",
        headers={"Authorization": f"Bearer {generate_admin_test_token}"},
    )
    assert response.status_code == expected_status
