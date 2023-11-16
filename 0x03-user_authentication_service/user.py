#!/usr/bin/env python3
"""
This module defines a SQLAlchemy model, `User` for a database table, `users`.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    A class used to represent a user in the database.

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

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=250), nullable=False)
    hashed_password = Column(String(length=250), nullable=False)
    session_id = Column(String(length=250), nullable=True)
    reset_token = Column(String(length=250), nullable=True)

    def __init__(self, *args, **kwargs):
        """Initialize a new `User` object."""
        self.__dict__.update(kwargs)

    def __repr__(self):
        """Return the canonical string representation of `User`."""
        return f"<User(name='{self.name}', email='{self.email}')>"

    def __str__(self):
        """Return a string representation of `User`."""
        return f"{self.name} <{self.email}>"
