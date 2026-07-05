from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order_item import OrderItem


class Product(TimestampMixin, Base):
    """
    Sellable product definition used in orders and invoices.
    """

    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("unit_price >= 0", name="products_unit_price_non_negative"),
        CheckConstraint("stock_quantity >= 0", name="products_stock_quantity_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(nullable=False, default=0, server_default="0")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
