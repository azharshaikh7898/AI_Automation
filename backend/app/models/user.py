from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.role import Role


class User(TimestampMixin, Base):
    """
    Application user account used for authentication and authorization.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users")
