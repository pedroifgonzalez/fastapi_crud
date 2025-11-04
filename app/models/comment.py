from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixin import SoftDeleteMixin, TimestampMixin


class Comment(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="fk_comments_user_id_users",
        ),
        nullable=False,
        index=True,
    )
    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "posts.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="fk_comments_post_id_posts",
        ),
        nullable=False,
        index=True,
    )
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
