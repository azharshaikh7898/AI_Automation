from datetime import datetime

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.sql.sqltypes import DateTime


NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(DeclarativeBase):
    """
    Base class for all ORM models.

    Provides consistent metadata and automatic table name generation.
    """

    metadata = metadata

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampMixin:
    """
    Reusable timestamp columns for auditable tables.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
