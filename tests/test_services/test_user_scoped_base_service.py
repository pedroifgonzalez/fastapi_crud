import pytest

from app.models.post import Post
from app.services.base import ServiceException
from app.services.base_user_scoped import UserScopedBaseService


async def test_find_one_for_user(db, test_user, test_post, test_user_2):
    post_user_scoped_service = UserScopedBaseService(db=db, model=Post)
    db_record = await post_user_scoped_service.find_one_for_user(
        id=test_post.id, user_id=test_user.id
    )

    assert db_record

    db_record = await post_user_scoped_service.find_one_for_user(
        id=test_post.id,
        user_id=test_user.id,
        eager_load=False,
    )
    assert db_record

    with pytest.raises(ServiceException) as error:
        await post_user_scoped_service.find_one_for_user(
            id=test_post.id, user_id=test_user_2.id
        )
    assert f"{test_post.__class__.__name__} with id {test_post.id} not found" in str(
        error
    )


async def test_update_for_user(db, test_user, test_post, test_user_2):
    post_user_scoped_service = UserScopedBaseService(db=db, model=Post)
    old_content = test_post.content
    await post_user_scoped_service.update_for_user(
        id=test_post.id,
        user_id=test_user.id,
        data={"content": "This is a modified post content"},
    )

    db_record = await db.get(Post, test_post.id)

    assert db_record.content != old_content
    with pytest.raises(ServiceException) as error:
        await post_user_scoped_service.find_one_for_user(
            id=test_post.id, user_id=test_user_2.id
        )
    assert f"{test_post.__class__.__name__} with id {test_post.id} not found" in str(
        error
    )


async def test_delete_for_user(db, test_user, test_post, test_user_2):
    post_user_scoped_service = UserScopedBaseService(db=db, model=Post)

    with pytest.raises(ServiceException) as error:
        await post_user_scoped_service.find_one_for_user(
            id=test_post.id, user_id=test_user_2.id
        )
    assert f"{test_post.__class__.__name__} with id {test_post.id} not found" in str(
        error
    )

    await post_user_scoped_service.delete_for_user(
        id=test_post.id, user_id=test_user.id
    )
    db_record = await db.get(Post, test_post.id)
    assert db_record.is_deleted
