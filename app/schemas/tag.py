from pydantic import BaseModel, Field

from app.utils.validators import NonEmptyString


class TagBase(BaseModel):
    name: NonEmptyString = Field(description="Tag's name", min_length=3)


class TagIn(TagBase):
    pass


class TagOut(TagBase):
    id: int = Field(description="Tag's identification number")
