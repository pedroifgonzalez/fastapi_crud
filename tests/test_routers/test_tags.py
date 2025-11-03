import pytest

TAGS_BASE_URL = "/tags"


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_tag")
async def test_tags_router_find_all(async_client):
    response = await async_client.get(f"{TAGS_BASE_URL}/")
    data = response.json()
    assert data.get("total") > 0


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_tag", "test_deleted_tag")
@pytest.mark.parametrize(
    "tag_id,expected_status",
    [
        (1, 200),
        (10, 404),  # deleted tag
        (999, 404),  # non-existent tag
    ],
)
async def test_tags_router_find_one(async_client, tag_id, expected_status):
    response = await async_client.get(f"{TAGS_BASE_URL}/{tag_id}")
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_user", "test_tag")
@pytest.mark.parametrize(
    "data,expected_status",
    [({"name": "ValidTag"}, 200), ({"name": "  "}, 422)],
)
async def test_tags_router_create(
    async_client, data, expected_status, generate_test_token
):
    response = await async_client.post(
        f"{TAGS_BASE_URL}/",
        json=data,
        headers={"Authorization": f"Bearer {generate_test_token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_tag", "test_tag")
@pytest.mark.parametrize(
    "tag_id,data,expected_status",
    [
        (1, {"name": "ModifiedTag"}, 200),
        (1, {"name": "   "}, 422),  # emtpy tag
        (999, {"name": "NewTag"}, 404),  # non-existent tag
    ],
)
async def test_tags_router_update(
    async_client, tag_id, data, expected_status, generate_test_token
):
    response = await async_client.put(
        f"{TAGS_BASE_URL}/{tag_id}",
        json=data,
        headers={"Authorization": f"Bearer {generate_test_token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.usefixtures("test_tag", "test_deleted_tag")
@pytest.mark.parametrize(
    "tag_id,expected_status",
    [
        (1, 200),
        (10, 200),
        (999, 404),  # non-existent tag
    ],
)
async def test_tags_router_delete(
    async_client, tag_id, expected_status, generate_test_token
):
    response = await async_client.delete(
        f"{TAGS_BASE_URL}/{tag_id}",
        headers={"Authorization": f"Bearer {generate_test_token}"},
    )
    assert response.status_code == expected_status
