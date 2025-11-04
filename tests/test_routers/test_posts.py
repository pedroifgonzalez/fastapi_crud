import pytest

from app.schemas.post import PostOut
from app.utils.pagination import PaginatedResponse

from .conftest import assert_output_schema

POSTS_BASE_URL = "/posts"


@pytest.mark.asyncio
async def test_posts_router_find_all(async_client, test_post):
    response = await async_client.get(f"{POSTS_BASE_URL}/")
    data = response.json()
    assert data.get("total") > 0
    assert_output_schema(data=data, schema=PaginatedResponse[PostOut])


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_post", "test_deleted_post")
@pytest.mark.parametrize(
    "post_id,expected_status",
    [
        (1, 200),
        (10, 404),  # deleted post
        (999, 404),  # non-existent post
    ],
)
async def test_posts_router_find_one(async_client, post_id, expected_status):
    response = await async_client.get(f"{POSTS_BASE_URL}/{post_id}")
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert_output_schema(data=data, schema=PostOut)


@pytest.mark.usefixtures("test_user", "test_tag")
@pytest.mark.parametrize(
    "data,expected_status",
    [
        (
            {"content": "This is a valid post without tags"},
            200,
        ),
        (
            {"tags_ids": [1]},
            # missing content
            422,
        ),
        (
            {"content": "  "},
            422,
        ),
        (
            {
                "content": "This is a post with invalid tags",
                "tags_ids": [999],  # non-existent tag
            },
            404,
        ),
    ],
    ids=["Valid post", "Missing content", "Empty content", "Invalid tags"],
)
async def test_posts_router_create(
    async_client, data, expected_status, generate_test_token
):
    response = await async_client.post(
        f"{POSTS_BASE_URL}/",
        json=data,
        headers={"Authorization": f"Bearer {generate_test_token}"},
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert_output_schema(data=data, schema=PostOut)


@pytest.mark.usefixtures("test_post", "test_post_2", "test_tag")
@pytest.mark.parametrize(
    "post_id,data,expected_status",
    [
        (
            1,
            {"content": "This is a new content for the post"},
            200,
        ),
        (
            1,
            {
                "tags_ids": [1],
            },
            200,
        ),
        (
            1,
            {
                "tags_ids": [999],  # non-existent tag
            },
            404,
        ),
        (
            999,  # non-existent post
            {
                "tags_ids": [1],
            },
            404,
        ),
        (
            2,  # non-owner post
            {
                "tags_ids": [1],
            },
            404,
        ),
    ],
    ids=[
        "Update content",
        "Update tags",
        "Non-existent tag",
        "Non-existent post",
        "Non-owner post",
    ],
)
async def test_posts_router_update(
    async_client, post_id, data, expected_status, generate_test_token
):
    response = await async_client.put(
        f"{POSTS_BASE_URL}/{post_id}",
        json=data,
        headers={"Authorization": f"Bearer {generate_test_token}"},
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert_output_schema(data=data, schema=PostOut)


@pytest.mark.usefixtures("test_post", "test_deleted_post", "test_post_2")
@pytest.mark.parametrize(
    "post_id,expected_status",
    [
        (1, 200),
        (10, 200),  # already deleted (silenced managed response)
        (999, 404),  # non-existent post
        (2, 404),  # non-owner post
    ],
)
async def test_posts_router_delete(
    async_client, post_id, expected_status, generate_test_token
):
    response = await async_client.delete(
        f"{POSTS_BASE_URL}/{post_id}",
        headers={"Authorization": f"Bearer {generate_test_token}"},
    )
    assert response.status_code == expected_status
