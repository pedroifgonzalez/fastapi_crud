import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.comment import CommentOut
from app.schemas.post import PostOut
from app.utils.validators import NonEmptyString

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


class UserBase(BaseModel):
    name: NonEmptyString = Field(description="User's full name", min_length=3)
    email: EmailStr = Field(description="User's email")


class UserIn(UserBase):
    password: str = Field(description="User's password")

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if not PASSWORD_REGEX.match(v):
            raise ValueError(
                "Password must contain at least 8 characters, including uppercase, lowercase, digit, and special symbol."
            )
        return v


class UserOut(UserBase):
    id: int = Field(description="User's identification number")
    posts: list[PostOut] = Field(description="User's posts")
    comments: list[CommentOut] = Field(description="User's comments")
