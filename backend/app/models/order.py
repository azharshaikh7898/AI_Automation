from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.invoice import Invoice
    from app.models.order_item import OrderItem
    from app.models.payment import Payment
    from app.models.user import User


class Order(TimestampMixin, Base):
    """
    Sales order header linked to a customer and optionally an account owner.
    """

    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'confirmed', 'processing', 'completed', 'cancelled')",
            name="orders_status_valid",
        ),
        CheckConstraint("total_amount >= 0", name="orders_total_amount_non_negative"),
        Index("ix_orders_customer_id_status", "customer_id", "status"),
        Index("ix_orders_created_by_id_status", "created_by_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    order_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
        server_default="draft",
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD", server_default="USD")
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    created_by: Mapped["User | None"] = relationship()
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
