from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://") and not database_url.startswith("postgresql+"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


normalized_database_url = _normalize_database_url(settings.database_url)

engine_kwargs: dict[str, object] = {
    "future": True,
    "pool_pre_ping": not normalized_database_url.startswith("sqlite"),
}
if normalized_database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(normalized_database_url, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()