from typing import Any

from fastapi import status
from sqlalchemy.sql import select, update

from app.services.base import BaseService, ServiceException, T
from app.services.mixin import UserScopedServiceMixin
from app.utils.constants import NOT_FOUND_ERROR


class UserScopedBaseService(BaseService[T], UserScopedServiceMixin):
    async def find_one_for_user(
        self, id: int, user_id: int, eager_load: bool = True
    ) -> T:
        if eager_load:
            stmt = self._get_select_with_relationships().where(self.model.id == id)  # type: ignore
        else:
            stmt = select(self.model)

        stmt = await self._apply_user_scope(stmt, user_id)

        result = await self.db.execute(stmt)
        db_record = result.scalar_one_or_none()

        if not db_record:
            raise ServiceException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=NOT_FOUND_ERROR.format(self.model_name, id),
            )

        return db_record

    async def update_for_user(self, id: int, user_id: int, data: dict[str, Any]) -> T:
        db_record = await self.find_one_for_user(id=id, user_id=user_id)

        for field, value in data.items():
            if hasattr(db_record, field):
                setattr(db_record, field, value)

        await self.db.flush()
        await self.db.commit()
        return await self.find_one_for_user(id=id, user_id=user_id)

    async def delete_for_user(self, id: int, user_id: int) -> None:
        db_record = await self.find_one_for_user(id=id, user_id=user_id)

        stmt = (
            update(self.model)
            .where(self.model.id == db_record.id)  # type: ignore
            .values(is_deleted=True)
        )
        await self.db.execute(stmt)
        await self.db.commit()
