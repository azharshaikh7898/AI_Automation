from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """
    Payload for user registration.
    """

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str | None = Field(default=None, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)
    role_name: str = Field(default="Sales Executive", min_length=2, max_length=50)

    @field_validator("first_name", "last_name", "role_name", mode="before")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        return value.strip()

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone_number(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None


class LoginRequest(BaseModel):
    """
    Payload for login using email and password.
    """

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class RefreshTokenRequest(BaseModel):
    """
    Payload for obtaining a new access token from a refresh token.
    """

    refresh_token: str = Field(..., min_length=1)


class TokenPairResponse(BaseModel):
    """
    JWT pair returned after successful authentication.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthenticatedUser(BaseModel):
    """
    Public authenticated user payload returned by auth-related APIs.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    role_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str | None
    is_active: bool
    is_superuser: bool


class AuthResponse(BaseModel):
    """
    Authentication response payload combining user info and token pair.
    """

    user: AuthenticatedUser
    tokens: TokenPairResponse
