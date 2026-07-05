from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerBase(BaseModel):
    """
    Shared customer fields used across create and update payloads.
    """

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, max_length=20)
    company_name: str | None = Field(default=None, max_length=255)
    assigned_user_id: int | None = None
    status: str = Field(default="lead", max_length=20)
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = None

    @field_validator("first_name", "last_name", "company_name", "source", mode="before")
    @classmethod
    def strip_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone_number(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value: str) -> str:
        return value.strip().lower()


class CustomerCreate(CustomerBase):
    """Create payload for customers."""


class CustomerUpdate(BaseModel):
    """
    Partial update payload for customers.
    """

    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, max_length=20)
    company_name: str | None = Field(default=None, max_length=255)
    assigned_user_id: int | None = None
    status: str | None = Field(default=None, max_length=20)
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = None

    @field_validator("first_name", "last_name", "company_name", "source", mode="before")
    @classmethod
    def strip_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_optional_phone_number(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("status", mode="before")
    @classmethod
    def normalize_optional_status(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().lower()


class CustomerRead(BaseModel):
    """
    Public customer representation returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    assigned_user_id: int | None
    first_name: str
    last_name: str
    email: EmailStr | None
    phone_number: str | None
    company_name: str | None
    status: str
    source: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
