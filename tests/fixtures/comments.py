import pytest

from app.models.comment import Comment


@pytest.fixture(scope="function")
async def test_comment(db, test_user):
    comment_record = Comment(content="This is a test comment", user=test_user)
    db.add(comment_record)
    await db.commit()
    await db.refresh(comment_record)
    yield comment_record


@pytest.fixture(scope="function")
async def test_deleted_comment(db, test_user):
    comment_record = Comment(
        id=10, content="This is a deleted test comment", user=test_user, is_deleted=True
    )
    db.add(comment_record)
    await db.commit()
    await db.refresh(comment_record)
    yield comment_record
