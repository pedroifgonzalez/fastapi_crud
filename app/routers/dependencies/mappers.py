from fastapi import Depends

from app.core.mappers.posts import PostMapper
from app.routers.dependencies.services import get_tag_service
from app.services.tags import TagsService


def get_post_mapper(tag_service: TagsService = Depends(get_tag_service)) -> PostMapper:
    return PostMapper(tag_service=tag_service)
