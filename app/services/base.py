from typing import Any, Generic, Type, TypeVar

from fastapi import status
from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import Select
from typing_extensions import Optional

from app.core.exceptions import AppException
from app.models.base import Base
from app.services.mixin import SoftDeleteFilterMixin
from app.utils.constants import NOT_FOUND_ERROR
from app.utils.pagination import PaginationParams

T = TypeVar("T", bound=Base)


class ServiceException(AppException):
    pass


class BaseService(Generic[T], SoftDeleteFilterMixin):
    _eager_load_relationships: list[str] = []

    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model
        self.model_name = model.__name__

    def _get_select_with_relationships(
        self, include_deleted: bool = False
    ) -> Select[tuple[T]]:
        """Build select statement with eager loading."""
        stmt = select(self.model)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted=include_deleted)
        for rel in self._eager_load_relationships:
            if hasattr(self.model, rel):
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        return stmt

    async def _get_select_with_pagination(
        self, stmt: Select, pagination: PaginationParams
    ) -> tuple[Result[tuple[T]], Optional[int]]:
        total = await self.db.scalar(select(func.count()).select_from(stmt.subquery()))
        result = await self.db.execute(
            stmt.limit(pagination.page_size).offset(
                (pagination.page - 1) * pagination.page_size
            )
        )
        return result, total

    async def find_all(
        self,
        eager_load: bool = True,
        pagination: Optional[PaginationParams] = None,
        include_deleted: bool = False,
    ) -> tuple[list[T], int]:
        """Get all records, optionally with relationships."""
        if eager_load and self._eager_load_relationships:
            stmt = self._get_select_with_relationships(include_deleted=include_deleted)
        else:
            stmt = select(self.model)
            stmt = self._apply_soft_delete_filter(stmt, include_deleted=include_deleted)

        total = None
        if pagination:
            result, total = await self._get_select_with_pagination(
                stmt=stmt, pagination=pagination
            )
        else:
            result = await self.db.execute(stmt)
        output = list(result.scalars().all())
        return output, total if total else len(output)

    async def find_one(
        self, id: int, eager_load: bool = True, include_deleted: bool = False
    ) -> Any | T:
        """Get a single record by ID, optionally with relationships."""
        if eager_load and self._eager_load_relationships:
            stmt = self._get_select_with_relationships(include_deleted=include_deleted).where(self.model.id == id)  # type: ignore
            result = await self.db.execute(stmt)
            db_record = result.scalar_one_or_none()
        else:
            stmt = select(self.model).where(self.model.id == id)  # type: ignore
            stmt = self._apply_soft_delete_filter(stmt, include_deleted=include_deleted)
            result = await self.db.execute(stmt)
            db_record = result.scalar_one_or_none()

        if not db_record:
            raise ServiceException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=NOT_FOUND_ERROR.format(self.model_name, id),
            )
        return db_record

    async def create(self, data: dict[str, Any], eager_load: bool = True) -> T:
        record = self.model(**data)
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return await self.find_one(id=record.id, eager_load=eager_load)  # type: ignore

    async def update(self, id: int, data: dict[str, Any]) -> T:
        db_record = await self.find_one(id=id)

        for field, value in data.items():
            if hasattr(db_record, field):
                setattr(db_record, field, value)

        await self.db.flush()
        await self.db.commit()
        return await self.find_one(id=id)

    async def delete(self, id: int) -> None:
        db_record = await self.find_one(id=id, eager_load=False, include_deleted=True)

        stmt = (
            update(self.model)
            .where(self.model.id == db_record.id)  # type: ignore
            .values(is_deleted=True)
        )
        await self.db.execute(stmt)
        await self.db.commit()
