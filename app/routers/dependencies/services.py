from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mappers.posts import PostMapper
from app.routers.dependencies.db import get_db
from app.services.comments import CommentService
from app.services.posts import PostService
from app.services.tags import TagsService
from app.services.users import UserService
from app.services.validators.integrity import PostIntegrityValidator


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_post_service(db: AsyncSession = Depends(get_db)) -> PostService:
    return PostService(db)


def get_tag_service(db: AsyncSession = Depends(get_db)) -> TagsService:
    return TagsService(db)


def get_comment_service(db: AsyncSession = Depends(get_db)) -> CommentService:
    return CommentService(db)


def get_post_mapper(tag_service: TagsService = Depends(get_tag_service)) -> PostMapper:
    return PostMapper(tag_service=tag_service)


def get_post_integrity_validator(
    db: AsyncSession = Depends(get_db),
) -> PostIntegrityValidator:
    return PostIntegrityValidator(db=db)
