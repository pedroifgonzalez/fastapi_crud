from fastapi import Depends

from app.core.mappers.auth import AuthMapper
from app.core.mappers.comments import CommentMapper
from app.core.mappers.posts import PostMapper
from app.core.mappers.tags import TagMapper
from app.core.mappers.users import UserMapper
from app.routers.dependencies.services import get_password_converter, get_tag_service
from app.services.converters.passwords import PasswordConverter
from app.services.tags import TagsService


def get_post_mapper(tag_service: TagsService = Depends(get_tag_service)) -> PostMapper:
    return PostMapper(tag_service=tag_service)


def get_tag_mapper() -> TagMapper:
    return TagMapper()


def get_comment_mapper() -> CommentMapper:
    return CommentMapper()


def get_user_mapper(
    password_converter: PasswordConverter = Depends(get_password_converter),
) -> UserMapper:
    return UserMapper(password_converter=password_converter)


def get_auth_mapper() -> AuthMapper:
    return AuthMapper()
