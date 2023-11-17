#!/usr/bin/env python3
"""This module defines `_hash_password`"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Return a salted, hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the `Auth` instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user and return the `User` object."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password).decode())

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False
