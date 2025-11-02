from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.base import BaseService


class UserService(BaseService[User]):

    _eager_load_relationships = ["comments", "posts"]

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)
