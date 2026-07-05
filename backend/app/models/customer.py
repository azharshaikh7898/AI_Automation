from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.interaction import Interaction
    from app.models.order import Order
    from app.models.task import Task
    from app.models.user import User


class Customer(TimestampMixin, Base):
    """
    Customer account managed by the sales and retention teams.
    """

    __tablename__ = "customers"
    __table_args__ = (
        CheckConstraint(
            "status IN ('lead', 'prospect', 'active', 'inactive', 'churned')",
            name="customer_status_valid",
        ),
        Index("ix_customers_assigned_user_id_status", "assigned_user_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    assigned_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="lead", server_default="lead")
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    assigned_user: Mapped["User | None"] = relationship()
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
    interactions: Mapped[list["Interaction"]] = relationship(back_populates="customer")
    tasks: Mapped[list["Task"]] = relationship(back_populates="customer")
