from functools import lru_cache
from typing import Any

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application settings loaded from environment variables.

    The settings object is intentionally comprehensive so the rest of the
    application can import configuration from one place instead of reading
    raw environment variables throughout the codebase.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    project_name: str = Field(default="Customer Retention & Sales Automation API")
    project_description: str = Field(
        default="Phase 1 backend for authentication, customer management, and sales workflows."
    )
    project_version: str = Field(default="1.0.0")
    api_v1_prefix: str = Field(default="/api/v1")

    backend_host: str = Field(default="0.0.0.0")
    backend_port: int = Field(default=8000)

    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="postgres")
    postgres_password: SecretStr = Field(default=SecretStr("postgres"))
    postgres_db: str = Field(default="customer_sales")

    jwt_secret_key: SecretStr = Field(default=SecretStr("change-me-in-production"))
    jwt_refresh_secret_key: SecretStr = Field(default=SecretStr("change-me-refresh-in-production"))
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    password_bcrypt_rounds: int = Field(default=12)
    log_level: str = Field(default="INFO")

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        allowed = {"development", "testing", "staging", "production"}
        normalized = value.strip().lower()
        if normalized not in allowed:
            allowed_values = ", ".join(sorted(allowed))
            raise ValueError(f"environment must be one of: {allowed_values}")
        return normalized

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            if not value.strip():
                return []
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        raise ValueError("cors_origins must be a comma-separated string or a list of strings")

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.strip().upper()

    @property
    def database_url(self) -> str:
        """
        SQLAlchemy connection string for the primary PostgreSQL database.
        """
        password = self.postgres_password.get_secret_value()
        return (
            f"postgresql+psycopg://{self.postgres_user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached settings instance for consistent application-wide access.
    """
    return Settings()


settings = get_settings()
