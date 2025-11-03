from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.services.base_user_scoped import UserScopedBaseService


class PostService(UserScopedBaseService[Post]):

    _eager_load_relationships = ["tags"]

    def __init__(self, db: AsyncSession):
        super().__init__(db, Post)
