from typing import Union

from app.models.tag import Tag
from app.schemas.tag import TagIn, TagOut, TagUpdate


class TagMapper:

    async def to_domain(self, data: Union[TagIn, TagUpdate]) -> dict:
        domain_data = data.model_dump(exclude_none=True)
        return domain_data

    def to_output(self, db_record: Tag) -> TagOut:
        data = {
            "id": db_record.id,
            "name": db_record.name,
        }
        return TagOut.model_validate(data)
