import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.main import app
from app.models.base import metadata
from app.routers.dependencies import get_db
from tests.fixtures import (
    test_comment,
    test_comment_2,
    test_deleted_comment,
    test_deleted_post,
    test_deleted_tag,
    test_post,
    test_post_2,
    test_tag,
    test_user,
    test_user_2,
)


@pytest.fixture(scope="function")
async def engine():
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db(engine):
    TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function", autouse=True)
def override_get_db(db):
    async def _get_db_override():
        yield db

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()


__all__ = [
    "test_user",
    "test_user_2",
    "test_post",
    "test_post_2",
    "test_tag",
    "test_deleted_tag",
    "test_comment",
    "test_deleted_post",
    "test_deleted_comment",
    "test_comment_2",
]
