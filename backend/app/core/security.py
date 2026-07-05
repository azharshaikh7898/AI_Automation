from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt
from jwt import InvalidTokenError

from app.core.config import settings

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against its bcrypt hash.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    """
    Create a bcrypt hash for a plaintext password.
    """
    salt = bcrypt.gensalt(rounds=settings.password_bcrypt_rounds)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def _build_token_payload(
    subject: str,
    expires_delta: timedelta,
    token_type: str,
    extra_claims: dict[str, Any] | None = None,
) -> dict[str, Any]:
    expires_at = datetime.now(UTC) + expires_delta
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    if extra_claims:
        payload.update(extra_claims)
    return payload


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    """
    Create a signed access token for the given subject.
    """
    payload = _build_token_payload(
        subject=subject,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type=ACCESS_TOKEN_TYPE,
        extra_claims=extra_claims,
    )
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    """
    Create a signed refresh token for the given subject.
    """
    payload = _build_token_payload(
        subject=subject,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type=REFRESH_TOKEN_TYPE,
        extra_claims=extra_claims,
    )
    return jwt.encode(
        payload,
        settings.jwt_refresh_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate an access token.
    """
    payload = jwt.decode(
        token,
        settings.jwt_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
    )
    _validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return payload


def decode_refresh_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a refresh token.
    """
    payload = jwt.decode(
        token,
        settings.jwt_refresh_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
    )
    _validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return payload


def _validate_token_type(payload: dict[str, Any], expected_type: str) -> None:
    token_type = payload.get("type")
    if token_type != expected_type:
        raise InvalidTokenError(f"Invalid token type: expected {expected_type}")
