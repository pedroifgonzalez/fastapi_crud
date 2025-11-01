from .comments import test_comment
from .posts import test_deleted_post, test_post
from .tags import test_tag
from .users import test_user

__all__ = [
    # Posts
    "test_post",
    "test_deleted_post",
    # Users
    "test_user",
    # Tags
    "test_tag",
    # Comments
    "test_comment",
]
