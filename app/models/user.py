from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.security.roles import UserRole
from app.models.base import Base
from app.models.mixin import SoftDeleteMixin, TimestampMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, server_default=UserRole.REGULAR
    )

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
