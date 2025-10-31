import pytest
from sqlalchemy import select

from app.models.post import Post
from app.services.base import ServiceException
from app.services.posts import PostService


@pytest.mark.asyncio
async def test_create(db, test_user, test_tag):
    post_service = PostService(db=db)
    data = {
        "content": "Hello this a new post!",
        "user": test_user,
        "tags": [test_tag],
    }
    record = await post_service.create(data=data)

    assert record.id
    assert record.content == "Hello this a new post!"
    assert record.user  # type: ignore
    assert record.user_id == test_user.id
    assert record.tags


@pytest.mark.asyncio
async def test_update(db, test_post):
    post_service = PostService(db=db)
    data = {
        "content": "This is a modified post content",
    }
    record = await post_service.update(id=test_post.id, data=data)

    assert record.content == "This is a modified post content"


@pytest.mark.asyncio
async def test_find_all(db, test_post):
    post_service = PostService(db=db)
    records = await post_service.find_all()

    assert len(records) == 1
    assert records[0].content == "This is a test post"


@pytest.mark.asyncio
async def test_find_one(db, test_post):
    post_service = PostService(db=db)
    record = await post_service.find_one(id=test_post.id)

    assert record.content == "This is a test post"


@pytest.mark.asyncio
async def test_delete(db, test_post):
    post_service = PostService(db=db)
    await post_service.delete(id=test_post.id)

    db_records = await db.execute(select(Post).where(id == test_post.id))
    assert len(list(db_records.scalars().all())) == 0


@pytest.mark.asyncio
async def test_non_existent(db, test_post):
    post_service = PostService(db=db)
    with pytest.raises(ServiceException) as exc:
        await post_service.find_one(id=999)
    assert str(exc.value) == "Post with id 999 not found"
