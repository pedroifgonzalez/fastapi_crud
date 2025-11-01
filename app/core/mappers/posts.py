from app.models.post import Post
from app.schemas.post import PostIn, PostOut
from app.services.tags import TagsService


class PostMapper:

    def __init__(self, tag_service: TagsService) -> None:
        self.tag_service = tag_service

    def to_domain(self, data: PostIn) -> dict:
        domain_data = data.model_dump()
        if tags_ids := domain_data.pop("tags_ids", []):
            tags = []
            for tag_id in tags_ids:
                tag = self.tag_service.find_one(id=tag_id)
                tags.append(tag)
            domain_data.pop("tags_ids")
            domain_data.update({"tags": tags})
        return domain_data

    def to_output(self, db_record: Post) -> PostOut:
        return PostOut.model_validate(db_record, from_attributes=True)
