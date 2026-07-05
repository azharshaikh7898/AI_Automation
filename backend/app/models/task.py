from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.trigger import Trigger
    from app.models.user import User


class Task(TimestampMixin, Base):
    """
    Actionable follow-up item assigned to a user for a customer workflow.
    """

    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed', 'cancelled')",
            name="tasks_status_valid",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'urgent')",
            name="tasks_priority_valid",
        ),
        Index("ix_tasks_assigned_user_id_status", "assigned_user_id", "status"),
        Index("ix_tasks_customer_id_due_date", "customer_id", "due_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    trigger_id: Mapped[int | None] = mapped_column(
        ForeignKey("triggers.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        server_default="pending",
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        server_default="medium",
    )
    due_date: Mapped[datetime | None] = mapped_column(nullable=True, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="tasks")
    assigned_user: Mapped["User | None"] = relationship()
    trigger: Mapped["Trigger | None"] = relationship()
