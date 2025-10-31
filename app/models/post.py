from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixin import SoftDeleteMixin, TimestampMixin


class Post(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="fk_posts_user_id_users",
        ),
        nullable=False,
        index=True,
    )
    tags = relationship("Tag", secondary="posts_tags_link", back_populates="posts")
