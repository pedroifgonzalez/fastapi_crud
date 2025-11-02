import pytest

COMMENTS_BASE_URL = "/comments"


@pytest.mark.asyncio
async def test_comments_router_find_all(async_client, test_comment):
    response = await async_client.get(f"{COMMENTS_BASE_URL}/")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_comment", "test_deleted_comment")
@pytest.mark.parametrize(
    "comment_id,expected_status",
    [
        (1, 200),
        (10, 404),  # deleted comment
        (999, 404),  # non-existent comment
    ],
)
async def test_comments_router_find_one(async_client, comment_id, expected_status):
    response = await async_client.get(f"{COMMENTS_BASE_URL}/{comment_id}")
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_user")
@pytest.mark.parametrize(
    "data,expected_status",
    [
        (
            {"content": "This is a valid comment", "user_id": 1},
            200,
        ),
        (
            {
                "content": "This is a valid with missing user_id",
                # no user_id
            },
            422,
        ),
        (
            {
                "content": "This is a valid comment with tags",
                "user_id": 999,  # non-existent user
            },
            404,
        ),
        (
            {
                "content": "  ",  # empty string
                "user_id": 1,
            },
            422,
        ),
    ],
)
async def test_comments_router_create(async_client, data, expected_status):
    response = await async_client.post(f"{COMMENTS_BASE_URL}/", json=data)
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_comment")
@pytest.mark.parametrize(
    "comment_id,data,expected_status",
    [
        (
            1,
            {"content": "This is a new content for the comment"},
            200,
        ),
        (
            999,  # non-existent comment
            {
                "tags_ids": [1],
            },
            404,
        ),
        (
            1,
            {
                "content": "  ",  # empty string
                "user_id": 1,
            },
            422,
        ),
    ],
)
async def test_comments_router_update(async_client, comment_id, data, expected_status):
    response = await async_client.put(f"{COMMENTS_BASE_URL}/{comment_id}", json=data)
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_comment", "test_deleted_comment")
@pytest.mark.parametrize(
    "comment_id,expected_status",
    [
        (1, 200),
        (10, 200),
        (999, 404),  # non-existent comment
    ],
)
async def test_comments_router_delete(async_client, comment_id, expected_status):
    response = await async_client.delete(f"{COMMENTS_BASE_URL}/{comment_id}")
    assert response.status_code == expected_status
