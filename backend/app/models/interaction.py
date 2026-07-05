from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.user import User


class Interaction(TimestampMixin, Base):
    """
    Logged customer touchpoint such as a call, email, meeting, or follow-up.
    """

    __tablename__ = "interactions"
    __table_args__ = (
        CheckConstraint(
            "interaction_type IN ('call', 'email', 'meeting', 'sms', 'note')",
            name="interactions_type_valid",
        ),
        Index("ix_interactions_customer_id_interaction_date", "customer_id", "interaction_date"),
        Index("ix_interactions_created_by_id_interaction_type", "created_by_id", "interaction_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    interaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    outcome: Mapped[str | None] = mapped_column(String(255), nullable=True)
    interaction_date: Mapped[datetime] = mapped_column(nullable=False, index=True)

    customer: Mapped["Customer"] = relationship(back_populates="interactions")
    created_by: Mapped["User | None"] = relationship()
