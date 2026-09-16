"""Database configuration for the asset register application."""

# pyright: reportMissingImports=false
# pylint: disable=import-error

from sqlalchemy import create_engine  # type: ignore[import-not-found]
from sqlalchemy.orm import declarative_base, sessionmaker  # type: ignore[import-not-found]
DATABASE_URL = "sqlite:///./assets.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False},)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()