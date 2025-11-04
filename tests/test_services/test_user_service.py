import pytest
from sqlalchemy import select

from app.core.config import settings
from app.models.user import User
from app.services.base import ServiceException
from app.services.users import UserService
from app.utils.pagination import PaginationParams


@pytest.mark.asyncio
async def test_create(db):
    user_service = UserService(db=db)
    data = {
        "name": "John Smith",
        "email": "johnsmith@gmail.com",
        "hashed_password": "testpaswordhashed",
    }
    record = await user_service.create(data=data)

    assert record.id
    assert record.name == "John Smith"
    assert record.email == "johnsmith@gmail.com"


@pytest.mark.asyncio
async def test_update(db, test_user):
    user_service = UserService(db=db)
    data = {
        "name": "Jane Chester",
    }
    record = await user_service.update(id=test_user.id, data=data)
    updated_record = await user_service.find_one(id=record.id)
    assert updated_record.name == "Jane Chester"


@pytest.mark.asyncio
@pytest.mark.skipif(
    "sqlite" in settings.DATABASE_URL,
    reason="SQLite does not reflect fast the updated_at",
)
async def test_updated_at(db, test_user):
    user_service = UserService(db=db)
    data = {
        "name": "Jane Chester",
    }
    record = await user_service.update(id=test_user.id, data=data)
    updated_record = await user_service.find_one(id=record.id)
    assert updated_record.created_at != updated_record.updated_at


@pytest.mark.asyncio
async def test_find_all(db, test_user):
    user_service = UserService(db=db)
    records, total = await user_service.find_all()

    assert total == 1
    assert records[0].name == "Jane Smith"


@pytest.mark.asyncio
async def test_find_all_pagination(db, test_multiple_users):
    user_service = UserService(db=db)
    records, total = await user_service.find_all()
    pagination = PaginationParams(page=1, page_size=2)
    records_with_pagination, total_with_pagination = await user_service.find_all(
        pagination=pagination
    )

    assert total_with_pagination == len(test_multiple_users) == total
    start = (pagination.page - 1) * pagination.page_size
    end = start + pagination.page_size
    assert records_with_pagination == records[start:end]

    pagination2 = PaginationParams(page=2, page_size=2)
    records_page2, _ = await user_service.find_all(pagination=pagination2)

    start2 = (pagination2.page - 1) * pagination2.page_size
    end2 = start2 + pagination2.page_size
    assert records_page2 == records[start2:end2]


@pytest.mark.asyncio
async def test_find_one(db, test_user):
    user_service = UserService(db=db)
    record = await user_service.find_one(id=test_user.id)

    assert record.name == "Jane Smith"


@pytest.mark.asyncio
async def test_delete(db, test_user):
    user_service = UserService(db=db)
    await user_service.delete(id=test_user.id)

    db_records = await db.execute(select(User).where(id == test_user.id))
    assert len(list(db_records.scalars().all())) == 0


@pytest.mark.asyncio
async def test_non_existent(db, test_post):
    user_service = UserService(db=db)
    with pytest.raises(ServiceException) as exc:
        await user_service.find_one(id=999)
    assert str(exc.value) == "404: User with id 999 not found"


@pytest.mark.asyncio
async def test_find_by_email(db, test_user):
    user_service = UserService(db=db)
    db_record = await user_service.find_by_email(email=test_user.email)
    assert db_record

    with pytest.raises(ServiceException):
        await user_service.find_by_email(email="nonexistentuser@gmail.com")
