from pydantic import BaseModel, EmailStr, Field

from app.schemas.comment import CommentOut
from app.schemas.post import PostOut
from app.utils.validators import NonEmptyString


class UserBase(BaseModel):
    name: NonEmptyString = Field(description="User's full name", min_length=3)
    email: EmailStr = Field(description="User's email")


class UserIn(UserBase):
    pass


class UserOut(UserBase):
    id: int = Field(description="User's identification number")
    posts: list[PostOut] = Field(description="User's posts")
    comments: list[CommentOut] = Field(description="User's comments")
