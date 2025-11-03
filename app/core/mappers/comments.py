from typing import Union

from app.models.comment import Comment
from app.schemas.comment import CommentIn, CommentOut, CommentUpdate


class CommentMapper:

    async def to_domain(self, data: Union[CommentIn, CommentUpdate]) -> dict:
        domain_data = data.model_dump(exclude_none=True)
        return domain_data

    def to_output(self, db_record: Comment) -> CommentOut:
        data = {
            "id": db_record.id,
            "content": db_record.content,
            "user_id": db_record.user_id,
            "post_id": db_record.post_id,
        }
        return CommentOut.model_validate(data)
