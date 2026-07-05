from collections.abc import Callable

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Security(oauth2_scheme),
) -> User:
    """
    Resolve the authenticated user from a bearer access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user_id = int(subject)
    except (InvalidTokenError, TypeError, ValueError):
        raise credentials_exception from None

    user = get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise credentials_exception

    return user


def require_roles(*role_names: str) -> Callable[..., User]:
    """
    Build a dependency that allows only the supplied role names.
    """
    allowed_roles = {role_name.strip().lower() for role_name in role_names}

    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.is_superuser:
            return current_user

        current_role_name = current_user.role.name.strip().lower()
        if current_role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_dependency
