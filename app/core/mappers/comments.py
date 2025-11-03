from typing import Optional, Union, overload

from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentIn, CommentOut, CommentUpdate


class CommentMapper:

    @overload
    async def to_domain(self, data: CommentIn, user: User) -> dict: ...

    @overload
    async def to_domain(self, data: CommentUpdate) -> dict: ...

    async def to_domain(
        self, data: Union[CommentIn, CommentUpdate], user: Optional[User] = None
    ) -> dict:
        domain_data = data.model_dump(exclude_none=True)
        if user:
            domain_data.update({"user_id": user.id})
        return domain_data

    def to_output(self, db_record: Comment) -> CommentOut:
        data = {
            "id": db_record.id,
            "content": db_record.content,
            "user_id": db_record.user_id,
            "post_id": db_record.post_id,
        }
        return CommentOut.model_validate(data)
