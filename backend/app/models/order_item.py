from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.product import Product


class OrderItem(TimestampMixin, Base):
    """
    Individual line item belonging to a sales order.
    """

    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="order_items_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="order_items_unit_price_non_negative"),
        CheckConstraint("line_total >= 0", name="order_items_line_total_non_negative"),
        Index("ix_order_items_order_id_product_id", "order_id", "product_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )

    order: Mapped["Order"] = relationship(back_populates="order_items")
    product: Mapped["Product"] = relationship(back_populates="order_items")
