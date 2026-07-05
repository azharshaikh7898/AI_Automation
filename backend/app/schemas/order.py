from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderItemBase(BaseModel):
    """
    Shared order item fields.
    """

    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Decimal | None = Field(default=None, ge=0)


class OrderItemCreate(OrderItemBase):
    """Create payload for order items."""


class OrderItemRead(BaseModel):
    """
    Public order item representation.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal
    created_at: datetime
    updated_at: datetime


class OrderBase(BaseModel):
    """
    Shared order fields.
    """

    customer_id: int
    created_by_id: int | None = None
    order_number: str = Field(..., min_length=1, max_length=50)
    status: str = Field(default="draft", max_length=20)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    notes: str | None = None

    @field_validator("order_number", "currency", mode="before")
    @classmethod
    def strip_and_normalize_code_fields(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value: str) -> str:
        return value.strip().lower()


class OrderCreate(OrderBase):
    """
    Create payload for orders.
    """

    items: list[OrderItemCreate] = Field(default_factory=list)


class OrderUpdate(BaseModel):
    """
    Partial update payload for orders.
    """

    customer_id: int | None = None
    created_by_id: int | None = None
    status: str | None = Field(default=None, max_length=20)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    notes: str | None = None

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_optional_currency(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().upper()

    @field_validator("status", mode="before")
    @classmethod
    def normalize_optional_status(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().lower()


class OrderRead(BaseModel):
    """
    Public order representation returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    created_by_id: int | None
    order_number: str
    status: str
    currency: str
    total_amount: Decimal
    notes: str | None
    created_at: datetime
    updated_at: datetime
    order_items: list[OrderItemRead] = Field(default_factory=list)
