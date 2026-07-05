from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TriggerBase(BaseModel):
    """
    Shared trigger fields.
    """

    name: str = Field(..., min_length=1, max_length=150)
    trigger_type: str = Field(..., min_length=1, max_length=50)
    description: str | None = None
    condition_expression: str | None = None
    delay_minutes: int = Field(default=0, ge=0)
    is_active: bool = True

    @field_validator("name", "trigger_type", "description", "condition_expression", mode="before")
    @classmethod
    def strip_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("trigger_type")
    @classmethod
    def normalize_trigger_type(cls, value: str) -> str:
        return value.strip().lower()


class TriggerCreate(TriggerBase):
    """Create payload for triggers."""


class TriggerUpdate(BaseModel):
    """
    Partial update payload for triggers.
    """

    name: str | None = Field(default=None, min_length=1, max_length=150)
    trigger_type: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    condition_expression: str | None = None
    delay_minutes: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

    @field_validator("name", "trigger_type", "description", "condition_expression", mode="before")
    @classmethod
    def strip_optional_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("trigger_type", mode="before")
    @classmethod
    def normalize_optional_trigger_type(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().lower()


class TriggerRead(BaseModel):
    """
    Public trigger payload returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    trigger_type: str
    description: str | None
    condition_expression: str | None
    delay_minutes: int
    is_active: bool
    created_at: datetime
    updated_at: datetime