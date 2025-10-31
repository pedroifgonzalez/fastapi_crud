import pytest

from app.models.tag import Tag


@pytest.fixture(scope="function")
async def test_tag(db):
    tag_record = Tag(name="TestTag")
    db.add(tag_record)
    await db.commit()
    await db.refresh(tag_record)
    yield tag_record
