from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.services.base import BaseService


class CommentService(BaseService[Comment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Comment)
