from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)
