from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.tag import Tag
from app.services.base import BaseService


class TagsService(BaseService[Tag]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Tag)
