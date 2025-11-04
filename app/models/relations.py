from sqlalchemy import Column, ForeignKey, Table

from app.models.base import Base

posts_tags_link = Table(
    "posts_tags_link",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id")),
    Column("tag_id", ForeignKey("tags.id")),
)
