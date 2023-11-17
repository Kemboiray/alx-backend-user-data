#!/usr/bin/env python3
"""
This module defines a SQLAlchemy model, `User` for a database table, `users`.
"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class"""
    pass


class User(Base):
    """
    This class represents a user in the database.

    Attributes
    ----------
    id : int
        a unique value for each user
    email : str
        the user's email address
    hashed_password : str
        the user's password (hashed)
    session_id : str
        a unique session ID for each user
    reset_token : str
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(250), nullable=False)
    session_id: Mapped[str] = mapped_column(String(250), nullable=True)
    reset_token: Mapped[str] = mapped_column(String(250), nullable=True)
