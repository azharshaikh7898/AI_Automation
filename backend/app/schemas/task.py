from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskBase(BaseModel):
    """
    Shared task fields.
    """

    customer_id: int
    assigned_user_id: int | None = None
    trigger_id: int | None = None
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: str = Field(default="pending", max_length=20)
    priority: str = Field(default="medium", max_length=20)
    due_date: datetime | None = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("priority")
    @classmethod
    def normalize_priority(cls, value: str) -> str:
        return value.strip().lower()


class TaskCreate(TaskBase):
    """Create payload for tasks."""


class TaskUpdate(BaseModel):
    """
    Partial update payload for tasks.
    """

    customer_id: int | None = None
    assigned_user_id: int | None = None
    trigger_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: str | None = Field(default=None, max_length=20)
    priority: str | None = Field(default=None, max_length=20)
    due_date: datetime | None = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_optional_text_fields(cls, value: str | None) -> str | None:
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

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_optional_priority(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().lower()


class TaskRead(BaseModel):
    """
    Public task payload returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    assigned_user_id: int | None
    trigger_id: int | None
    title: str
    description: str | None
    status: str
    priority: str
    due_date: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime