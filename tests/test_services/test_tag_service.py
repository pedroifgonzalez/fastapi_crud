import pytest
from sqlalchemy import select

from app.core.config import settings
from app.models.tag import Tag
from app.services.base import ServiceException
from app.services.tags import TagsService
from app.utils.pagination import PaginationParams


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
    updated_record = await tag_service.find_one(id=record.id)
    assert updated_record.name == "ModifiedTag"


@pytest.mark.asyncio
@pytest.mark.skipif(
    "sqlite" in settings.DATABASE_URL,
    reason="SQLite does not reflect fast the updated_at",
)
async def test_updated_at(db, test_tag):
    tag_service = TagsService(db=db)
    data = {
        "name": "ModifiedTag",
    }
    record = await tag_service.update(id=test_tag.id, data=data)
    await db.refresh(record)
    updated_record = await tag_service.find_one(id=record.id)
    assert updated_record.created_at != updated_record.updated_at


@pytest.mark.asyncio
async def test_find_all(db, test_tag):
    tag_service = TagsService(db=db)
    records, total = await tag_service.find_all()

    assert total == 1
    assert records[0].name == "TestTag"


@pytest.mark.asyncio
async def test_find_all_pagination(db, test_multiple_tags):
    tag_service = TagsService(db=db)
    records, total = await tag_service.find_all()
    pagination = PaginationParams(page=1, page_size=2)
    records_with_pagination, total_with_pagination = await tag_service.find_all(
        pagination=pagination
    )

    assert total_with_pagination == len(test_multiple_tags) == total
    start = (pagination.page - 1) * pagination.page_size
    end = start + pagination.page_size
    assert records_with_pagination == records[start:end]

    pagination2 = PaginationParams(page=2, page_size=2)
    records_page2, _ = await tag_service.find_all(pagination=pagination2)

    start2 = (pagination2.page - 1) * pagination2.page_size
    end2 = start2 + pagination2.page_size
    assert records_page2 == records[start2:end2]


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
