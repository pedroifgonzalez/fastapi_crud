import pytest
from sqlalchemy import select

from app.models.user import User
from app.services.base import ServiceException
from app.services.users import UserService


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

    await db.refresh(record)

    assert record.name == "Jane Chester"
    updated_record = await user_service.find_one(id=record.id)
    assert updated_record.created_at != updated_record.updated_at


@pytest.mark.asyncio
async def test_find_all(db, test_user):
    user_service = UserService(db=db)
    records, total = await user_service.find_all()

    assert total == 1
    assert records[0].name == "Jane Smith"


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
