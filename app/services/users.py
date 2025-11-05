from typing import Optional

from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.user import User
from app.services.base import BaseService, ServiceException
from app.utils.constants import EMAIL_NOT_FOUND_ERROR


class UserService(BaseService[User]):

    _eager_load_relationships = ["comments", "posts"]

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def find_by_email(
        self,
        email: str,
        raise_custom: Optional[AppException] = None,
        include_deleted: bool = False,
    ) -> User:
        stmt = select(User).where(User.email == email)
        stmt = self._apply_soft_delete_filter(
            stmt=stmt, include_deleted=include_deleted
        )
        result = await self.db.execute(stmt)
        db_record = result.scalar_one_or_none()
        if not db_record:
            raise raise_custom or ServiceException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=EMAIL_NOT_FOUND_ERROR.format(email),
            )
        return db_record
