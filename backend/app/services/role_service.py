from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role


DEFAULT_ROLES = {
    "Admin": "Full system access with elevated privileges.",
    "Manager": "Can manage team data and oversee customer activity.",
    "Sales Executive": "Can manage customers, orders, and interactions.",
}


def ensure_default_roles(db: Session) -> None:
    """
    Seed the built-in application roles if they are missing.
    """
    existing_role_names = set(db.scalars(select(Role.name)).all())
    created_role = False

    for role_name, description in DEFAULT_ROLES.items():
        if role_name in existing_role_names:
            continue
        db.add(Role(name=role_name, description=description))
        created_role = True

    if created_role:
        db.commit()
