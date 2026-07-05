from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    """
    Shared product payload fields.
    """

    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    unit_price: Decimal = Field(..., ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("sku")
    @classmethod
    def normalize_sku(cls, value: str) -> str:
        return value.strip().upper()


class ProductCreate(ProductBase):
    """Create payload for products."""


class ProductUpdate(BaseModel):
    """
    Partial update payload for products.
    """

    name: str | None = Field(default=None, min_length=1, max_length=255)
    sku: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    unit_price: Decimal | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_optional_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("sku", mode="before")
    @classmethod
    def normalize_optional_sku(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().upper()


class ProductRead(BaseModel):
    """
    Public product payload returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    description: str | None
    unit_price: Decimal
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
