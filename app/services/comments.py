from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.services.base_user_scoped import UserScopedBaseService


class CommentService(UserScopedBaseService[Comment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Comment)
