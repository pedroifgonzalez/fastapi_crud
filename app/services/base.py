from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select

from app.models.base import Base
from app.utils.constants import NOT_FOUND_ERROR

T = TypeVar("T", bound=Base)


class ServiceException(Exception):
    pass


class BaseService(Generic[T]):
    _eager_load_relationships: list[str] = []

    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model
        self.model_name = model.__name__

    def _get_select_with_relationships(self) -> Select[tuple[T]]:
        """Build select statement with eager loading."""
        stmt = select(self.model)

        for rel in self._eager_load_relationships:
            if hasattr(self.model, rel):
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        return stmt

    async def find_all(self, eager_load: bool = True) -> list[T]:
        """Get all records, optionally with relationships."""
        if eager_load and self._eager_load_relationships:
            stmt = self._get_select_with_relationships()
        else:
            stmt = select(self.model)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def find_one(self, id: int, eager_load: bool = True) -> Any | T:
        """Get a single record by ID, optionally with relationships."""
        if eager_load and self._eager_load_relationships:
            stmt = self._get_select_with_relationships().where(self.model.id == id)  # type: ignore
            result = await self.db.execute(stmt)
            db_record = result.scalar_one_or_none()
        else:
            db_record = await self.db.get(self.model, id)

        if not db_record:
            raise ServiceException(NOT_FOUND_ERROR.format(self.model_name, id))
        return db_record

    async def create(self, data: dict[str, Any]) -> T:
        record = self.model(**data)
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def update(self, id: int, data: dict[str, Any]) -> T:
        db_record = await self.find_one(id=id, eager_load=False)

        stmt = update(self.model).where(self.model.id == db_record.id).values(**data)  # type: ignore
        await self.db.execute(stmt)
        await self.db.commit()

        return await self.find_one(id=id)

    async def delete(self, id: int) -> None:
        db_record = await self.find_one(id=id, eager_load=False)

        stmt = (
            update(self.model)
            .where(self.model.id == db_record.id)  # type: ignore
            .values(is_deleted=True)
        )
        await self.db.execute(stmt)
        await self.db.commit()
