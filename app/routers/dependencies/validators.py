from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.dependencies.db import get_db
from app.services.validators.business import BaseBusinessValidator
from app.services.validators.integrity import (
    CommentIntegrityValidator,
    PostIntegrityValidator,
)


def get_post_integrity_validator(
    db: AsyncSession = Depends(get_db),
) -> PostIntegrityValidator:
    return PostIntegrityValidator(db=db)


def get_comment_integrity_validator(
    db: AsyncSession = Depends(get_db),
) -> CommentIntegrityValidator:
    return CommentIntegrityValidator(db=db)


def get_business_validator() -> BaseBusinessValidator:
    return BaseBusinessValidator()
