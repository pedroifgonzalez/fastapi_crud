import pytest
from sqlalchemy import select

from app.models.tag import Tag
from app.services.base import ServiceException
from app.services.tags import TagsService


@pytest.mark.asyncio
async def test_create(db):
    tag_service = TagsService(db=db)
    data = {
        "name": "NewTag",
    }
    record = await tag_service.create(data=data)

    assert record.id
    assert record.name == "NewTag"


@pytest.mark.asyncio
async def test_update(db, test_tag):
    tag_service = TagsService(db=db)
    data = {
        "name": "ModifiedTag",
    }
    record = await tag_service.update(id=test_tag.id, data=data)

    assert record.name == "ModifiedTag"


@pytest.mark.asyncio
async def test_find_all(db, test_tag):
    tag_service = TagsService(db=db)
    records = await tag_service.find_all()

    assert len(records) == 1
    assert records[0].name == "TestTag"


@pytest.mark.asyncio
async def test_find_one(db, test_tag):
    tag_service = TagsService(db=db)
    record = await tag_service.find_one(id=test_tag.id)

    assert record.name == "TestTag"


@pytest.mark.asyncio
async def test_delete(db, test_tag):
    tag_service = TagsService(db=db)
    await tag_service.delete(id=test_tag.id)

    db_records = await db.execute(select(Tag).where(id == test_tag.id))
    assert len(list(db_records.scalars().all())) == 0


@pytest.mark.asyncio
async def test_non_existent(db, test_post):
    tag_service = TagsService(db=db)
    with pytest.raises(ServiceException) as exc:
        await tag_service.find_one(id=999)
    assert str(exc.value) == "404: Tag with id 999 not found"
