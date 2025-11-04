import pytest

from app.models.tag import Tag


@pytest.fixture(scope="function")
async def test_tag(db):
    tag_record = Tag(name="TestTag")
    db.add(tag_record)
    await db.commit()
    await db.refresh(tag_record)
    yield tag_record


@pytest.fixture(scope="function")
async def test_deleted_tag(db):
    post_record = Tag(id=10, name="TestDeletedTag", is_deleted=True)
    db.add(post_record)
    await db.commit()
    await db.refresh(post_record)
    yield post_record


@pytest.fixture(scope="function")
async def test_multiple_tags(db):
    number_of_tags = 30
    tags = []
    for number in range(1, number_of_tags):
        tag = Tag(name="TestTag")
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        tags.append(tag)
    yield tags
