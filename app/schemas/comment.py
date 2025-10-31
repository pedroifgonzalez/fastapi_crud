from pydantic import BaseModel, Field

from app.utils.validators import NonEmptyString


class CommentBase(BaseModel):
    content: NonEmptyString = Field(description="Comment's content", min_length=10)
    user_id: int = Field(description="User, author of the comment")


class CommentIn(CommentBase):
    pass


class CommentOut(CommentBase):
    id: int = Field(description="Comment's identification number")
