"""SQLAlchemy models for the asset register."""
# pylint: disable=import-error
# pyright: reportMissingImports=false
from sqlalchemy import Column, Integer, String
from database import Base


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, unique=True, nullable=False, index=True)
    type = Column(String, nullable=False)
    model = Column(String, nullable=False)
    status = Column(String, nullable=False, default="In Use")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="staff")