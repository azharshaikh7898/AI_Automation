from __future__ import annotations

from typing import Final

from fastapi import HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenPairResponse
from app.services.role_service import ensure_default_roles


DEFAULT_USER_ROLE: Final[str] = "Sales Executive"


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Fetch a user by primary key.
    """
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Fetch a user by email address.
    """
    statement = select(User).where(User.email == email.strip().lower())
    return db.scalar(statement)


def _get_role_by_name(db: Session, role_name: str) -> Role | None:
    normalized_role_name = role_name.strip()
    statement = select(Role).where(Role.name == normalized_role_name)
    return db.scalar(statement)


def create_user(db: Session, payload: RegisterRequest) -> User:
    """
    Create a user account after validating uniqueness and role membership.
    """
    ensure_default_roles(db)

    email = payload.email.strip().lower()
    if get_user_by_email(db, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    role_name = payload.role_name.strip() or DEFAULT_USER_ROLE
    role = _get_role_by_name(db, role_name)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested role does not exist",
        )

    user = User(
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=email,
        phone_number=payload.phone_number.strip() if payload.phone_number else None,
        password_hash=get_password_hash(payload.password),
        role_id=role.id,
        is_active=True,
        is_superuser=role.name == "Admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Validate user credentials and return the matching user on success.
    """
    user = get_user_by_email(db, email)
    if user is None or not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def issue_token_pair(user: User) -> TokenPairResponse:
    """
    Create a signed access/refresh token pair for a user.
    """
    token_subject = str(user.id)
    extra_claims = {
        "role": user.role.name,
        "email": user.email,
        "is_superuser": user.is_superuser,
    }
    return TokenPairResponse(
        access_token=create_access_token(token_subject, extra_claims=extra_claims),
        refresh_token=create_refresh_token(token_subject, extra_claims=extra_claims),
    )


def refresh_user_tokens(db: Session, refresh_token: str) -> TokenPairResponse:
    """
    Validate a refresh token and return a fresh token pair.
    """
    try:
        payload = decode_refresh_token(refresh_token)
        subject = payload.get("sub")
        if subject is None:
            raise InvalidTokenError("Refresh token subject is missing")
        user_id = int(subject)
    except (InvalidTokenError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return issue_token_pair(user)
