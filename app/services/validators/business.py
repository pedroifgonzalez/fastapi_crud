from typing import Any, Generic, TypeVar

from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.base import Base
from app.utils.constants import ALREADY_EXISTENT, NOT_FOUND_ERROR

T = TypeVar("T", bound=Base)


class BusinessException(AppException):
    pass


class BaseBusinessValidator(Generic[T]):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def check_not_deleted(self, db_record: T) -> None:
        if db_record.is_deleted:  # type: ignore
            raise BusinessException(
                status_code=404,
                detail=NOT_FOUND_ERROR.format(
                    db_record.__class__.__name__, db_record.id  # type: ignore
                ),
            )

    async def check_not_existent(self, model: T, field: str, value: Any) -> None:
        stmt = select(model).where(getattr(model, field) == value)  # type: ignore
        result = await self.db.execute(stmt)
        db_record = result.scalar_one_or_none()
        if db_record:
            raise BusinessException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ALREADY_EXISTENT.format(
                    model.__name__,
                    field,
                    value,
                ),
            )
