from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.dependencies.db import get_db
from app.services.validators.integrity import PostIntegrityValidator


def get_post_integrity_validator(
    db: AsyncSession = Depends(get_db),
) -> PostIntegrityValidator:
    return PostIntegrityValidator(db=db)
