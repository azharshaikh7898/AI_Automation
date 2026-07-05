from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Role(TimestampMixin, Base):
    """
    RBAC role definition used to authorize application users.
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")
