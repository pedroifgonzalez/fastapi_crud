import pytest
from sqlalchemy import select

from app.core.config import settings
from app.models.comment import Comment
from app.services.base import ServiceException
from app.services.comments import CommentService


@pytest.mark.asyncio
async def test_create(db, test_user, test_post):
    comment_service = CommentService(db=db)
    data = {
        "content": "This is a new comment",
        "user": test_user,
        "post": test_post,
    }
    record = await comment_service.create(data=data)

    assert record.id


@pytest.mark.asyncio
async def test_update(db, test_comment):
    comment_service = CommentService(db=db)
    data = {
        "content": "Updated comment",
    }
    await comment_service.update(id=test_comment.id, data=data)
    updated_record = await comment_service.find_one(id=test_comment.id)
    assert updated_record.content == "Updated comment"


@pytest.mark.asyncio
@pytest.mark.skipif(
    "sqlite" in settings.DATABASE_URL,
    reason="SQLite does not reflect fast the updated_at",
)
async def test_updated_at(db, test_comment):
    comment_service = CommentService(db=db)
    data = {
        "content": "Updated comment",
    }
    await comment_service.update(id=test_comment.id, data=data)
    updated_record = await comment_service.find_one(id=test_comment.id)
    assert updated_record.created_at != updated_record.updated_at


@pytest.mark.asyncio
async def test_find_all(db, test_comment):
    comment_service = CommentService(db=db)
    records, total = await comment_service.find_all()

    assert total == 1
    assert records[0].content == "This is a test comment"


@pytest.mark.asyncio
async def test_find_one(db, test_comment):
    comment_service = CommentService(db=db)
    record = await comment_service.find_one(id=test_comment.id)

    assert record.content == "This is a test comment"


@pytest.mark.asyncio
async def test_delete(db, test_comment):
    comment_service = CommentService(db=db)
    await comment_service.delete(id=test_comment.id)

    db_records = await db.execute(select(Comment).where(id == test_comment.id))
    assert len(list(db_records.scalars().all())) == 0


@pytest.mark.asyncio
async def test_non_existent(db, test_post):
    comment_service = CommentService(db=db)
    with pytest.raises(ServiceException) as exc:
        await comment_service.find_one(id=999)
    assert str(exc.value) == "404: Comment with id 999 not found"
