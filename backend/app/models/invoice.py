from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order import Order


class Invoice(TimestampMixin, Base):
    """
    Billing document generated for a sales order.
    """

    __tablename__ = "invoices"
    __table_args__ = (
        CheckConstraint("amount_due >= 0", name="invoices_amount_due_non_negative"),
        CheckConstraint(
            "status IN ('draft', 'issued', 'paid', 'overdue', 'cancelled')",
            name="invoices_status_valid",
        ),
        Index("ix_invoices_order_id_status", "order_id", "status"),
        Index("ix_invoices_due_date_status", "due_date", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    issue_date: Mapped[date] = mapped_column(nullable=False)
    due_date: Mapped[date] = mapped_column(nullable=False, index=True)
    amount_due: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="invoices")
