from typing import Union

from app.models.post import Post
from app.schemas.post import PostIn, PostOut, PostUpdate
from app.services.tags import TagsService


class PostMapper:

    def __init__(self, tag_service: TagsService) -> None:
        self.tag_service = tag_service

    async def to_domain(self, data: Union[PostIn, PostUpdate]) -> dict:
        domain_data = data.model_dump(exclude_none=True)
        if tags_ids := domain_data.pop("tags_ids", []):
            tags = []
            for tag_id in tags_ids:
                tag = await self.tag_service.find_one(id=tag_id)
                tags.append(tag)
            domain_data.update({"tags": tags})
        return domain_data

    def to_output(self, db_record: Post) -> PostOut:
        data = {
            "id": db_record.id,
            "content": db_record.content,
            "user_id": db_record.user_id,
            "tags_ids": [tag.id for tag in db_record.tags],
        }
        return PostOut.model_validate(data)
