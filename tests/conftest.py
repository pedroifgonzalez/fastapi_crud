import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.base import metadata
from tests.fixtures import (
    test_comment,
    test_deleted_comment,
    test_deleted_post,
    test_deleted_tag,
    test_post,
    test_tag,
    test_user,
)


@pytest.fixture(scope="function")
async def engine():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
        await engine.dispose()


@pytest.fixture(scope="function")
async def db(engine):
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


__all__ = [
    "test_user",
    "test_post",
    "test_tag",
    "test_deleted_tag",
    "test_comment",
    "test_deleted_post",
    "test_deleted_comment",
]
