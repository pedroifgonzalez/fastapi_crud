from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User

posts_tags_link = Table(
    "posts_tags_link",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id")),
    Column("tag_id", ForeignKey("tags.id")),
)

User.posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
Post.user = relationship("User", back_populates="posts")
User.comments = relationship(
    "Comment", back_populates="user", cascade="all, delete-orphan"
)
Comment.user = relationship("User", back_populates="comments")
