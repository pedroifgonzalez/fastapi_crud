from .comments import test_comment, test_comment_2, test_deleted_comment
from .posts import test_deleted_post, test_post, test_post_2
from .tags import test_deleted_tag, test_multiple_tags, test_tag
from .users import test_deleted_user, test_multiple_users, test_user, test_user_2

__all__ = [
    # Posts
    "test_post",
    "test_deleted_post",
    "test_post_2",
    # Users
    "test_user",
    "test_user_2",
    "test_multiple_users",
    "test_deleted_user",
    # Tags
    "test_tag",
    "test_deleted_tag",
    "test_multiple_tags",
    # Comments
    "test_comment",
    "test_deleted_comment",
    "test_comment_2",
]
