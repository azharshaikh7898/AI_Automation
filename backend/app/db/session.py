from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine = None
SessionLocal = None


def _get_session_factory() -> sessionmaker[Session]:
    """
    Lazily create the SQLAlchemy engine and session factory.

    This keeps imports lightweight and allows tests to override database
    dependencies without opening a real PostgreSQL connection at import time.
    """
    global engine, SessionLocal

    if SessionLocal is None:
        engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            future=True,
        )
        SessionLocal = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=Session,
        )

    return SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a transactional database session.

    Sessions are always closed after use. Commit and rollback control stays in
    the service layer so request handlers remain thin and explicit.
    """
    session_factory = _get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
