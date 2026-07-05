from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    AuthenticatedUser,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenPairResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_user,
    issue_token_pair,
    refresh_user_tokens,
)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """
    Register a new user and return the initial token pair.
    """
    user = create_user(db, payload)
    return AuthResponse(user=AuthenticatedUser.model_validate(user), tokens=issue_token_pair(user))


@router.post("/login", response_model=AuthResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """
    Authenticate a user using email and password.
    """
    user = authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthResponse(user=AuthenticatedUser.model_validate(user), tokens=issue_token_pair(user))


@router.post("/refresh", response_model=TokenPairResponse)
def refresh_tokens(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> TokenPairResponse:
    """
    Exchange a refresh token for a new token pair.
    """
    return refresh_user_tokens(db, payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(_: User = Depends(get_current_user)) -> Response:
    """
    Stateless logout endpoint. The client discards its tokens after success.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
