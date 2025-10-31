import pytest

from app.models.post import Post


@pytest.fixture(scope="function")
async def test_post(db, test_user):
    post_record = Post(content="This is a test post", user=test_user)
    db.add(post_record)
    await db.commit()
    await db.refresh(post_record)
    yield post_record
