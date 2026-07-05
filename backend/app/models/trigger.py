from sqlalchemy import Boolean, CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Trigger(TimestampMixin, Base):
    """
    Automation rule definition used to initiate retention and sales workflows.
    """

    __tablename__ = "triggers"
    __table_args__ = (
        CheckConstraint(
            "trigger_type IN ('customer_created', 'order_created', 'payment_failed', 'invoice_overdue', 'inactive_customer')",
            name="triggers_type_valid",
        ),
        CheckConstraint("delay_minutes >= 0", name="triggers_delay_minutes_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    condition_expression: Mapped[str | None] = mapped_column(Text, nullable=True)
    delay_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
