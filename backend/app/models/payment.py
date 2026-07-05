from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order import Order


class Payment(TimestampMixin, Base):
    """
    Payment record associated with a sales order.
    """

    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="payments_amount_non_negative"),
        CheckConstraint(
            "status IN ('pending', 'authorized', 'paid', 'failed', 'refunded')",
            name="payments_status_valid",
        ),
        Index("ix_payments_order_id_status", "order_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        server_default="pending",
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    transaction_reference: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    order: Mapped["Order"] = relationship(back_populates="payments")
