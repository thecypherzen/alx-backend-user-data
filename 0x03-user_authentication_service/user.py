#!/usr/bin/env python3
"""User DB Model"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """The base class"""
    pass


class User(Base):
    """User Classs"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(250),
                                                 nullable=False)
    session_id: Mapped[str] = mapped_column(String(250))
    reset_token: Mapped[str] = mapped_column(String(250))
