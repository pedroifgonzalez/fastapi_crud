from typing import Optional

from pydantic import BaseModel, Field

from app.utils.validators import NonEmptyString


class PostBase(BaseModel):
    content: NonEmptyString = Field(description="Post's content", min_length=10)
    user_id: int = Field(description="User, author of the post")
    tags_ids: Optional[list[int]] = Field(
        default=None, description="List of tags associated to this post"
    )


class PostIn(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[NonEmptyString] = Field(
        None, description="Post's content", min_length=10
    )
    tags_ids: Optional[list[int]] = Field(
        default=None, description="List of tags associated to this post"
    )


class PostOut(PostBase):
    id: int = Field(description="Post's identification number")
