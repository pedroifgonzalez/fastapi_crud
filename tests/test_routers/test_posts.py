import pytest

POSTS_BASE_URL = "/posts"


@pytest.mark.asyncio
async def test_posts_router_find_all(async_client, test_post):
    response = await async_client.get(f"{POSTS_BASE_URL}/")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


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


@pytest.mark.usefixtures("test_user", "test_tag")
@pytest.mark.parametrize(
    "data,expected_status",
    [
        (
            {"content": "This is a valid post without tags", "user_id": 1},
            200,
        ),
        (
            {
                "content": "This is a valid post with tags",
                "user_id": 1,
                "tags_ids": [1],
            },
            200,
        ),
        (
            {
                "content": "This is a valid with missing user_id",
                "tags_ids": [1],
                # no user_id
            },
            422,
        ),
        (
            {
                "content": "This is a valid post with tags",
                "user_id": 999,  # non-existent user
                "tags_ids": [1],
            },
            404,
        ),
        (
            {
                "content": "This is a valid post with tags",
                "user_id": 1,
                "tags_ids": [999],  # non-existent tag
            },
            404,
        ),
    ],
)
async def test_posts_router_create(async_client, data, expected_status):
    response = await async_client.post(f"{POSTS_BASE_URL}/", json=data)
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_post", "test_tag")
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
    ],
)
async def test_posts_router_update(async_client, post_id, data, expected_status):
    response = await async_client.put(f"{POSTS_BASE_URL}/{post_id}", json=data)
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_post", "test_deleted_post")
@pytest.mark.parametrize(
    "post_id,expected_status",
    [
        (1, 200),
        (10, 200),
        (999, 404),  # non-existent post
    ],
)
async def test_posts_router_delete(async_client, post_id, expected_status):
    response = await async_client.delete(f"{POSTS_BASE_URL}/{post_id}")
    assert response.status_code == expected_status
