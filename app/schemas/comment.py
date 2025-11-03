from typing import Optional

from pydantic import BaseModel, Field

from app.utils.validators import NonEmptyString


class CommentBase(BaseModel):
    content: NonEmptyString = Field(description="Comment's content", min_length=10)
    user_id: int = Field(description="User, author of the comment")
    post_id: int = Field(description="Post to be commented on")


class CommentIn(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[NonEmptyString] = Field(
        None, description="Comment's content", min_length=10
    )


class CommentOut(CommentBase):
    id: int = Field(description="Comment's identification number")
