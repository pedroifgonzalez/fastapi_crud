import pytest

from app.models.comment import Comment


@pytest.fixture(scope="function")
async def test_comment(db, test_user, test_post):
    comment_record = Comment(
        content="This is a test comment", user=test_user, post=test_post
    )
    db.add(comment_record)
    await db.commit()
    await db.refresh(comment_record)
    yield comment_record


@pytest.fixture(scope="function")
async def test_deleted_comment(db, test_user, test_post):
    comment_record = Comment(
        id=10,
        content="This is a deleted test comment",
        user=test_user,
        is_deleted=True,
        post=test_post,
    )
    db.add(comment_record)
    await db.commit()
    await db.refresh(comment_record)
    yield comment_record
