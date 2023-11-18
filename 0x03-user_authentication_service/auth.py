#!/usr/bin/env python3
"""This module defines `_hash_password`"""

import bcrypt
import typing as t
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Return a salted, hashed password, which is a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return a string representation of a new UUID."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the `Auth` instance."""
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

    def create_session(self, email: str) -> t.Union[str, None]:
        """Create a session ID for the user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            setattr(user, "session_id", session_id)
            return session_id
        except NoResultFound:
            return

    def get_user_from_session_id(
            self,
            session_id: t.Union[str, None] = None) -> t.Union[User, None]:
        """Return the corresponding user from the session ID."""
        if session_id is not None:
            try:
                return self._db.find_user_by(session_id=session_id)
            except NoResultFound:
                return

    def destroy_session(self, user_id: int) -> None:
        """Destroy the user session."""
        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, "session_id", None)
        except NoResultFound:
            return

    def get_reset_password_token(self, email: str) -> str:
        """Return the reset token."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            setattr(user, "reset_token", reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password."""
        try:
            assert reset_token and isinstance(reset_token, str)
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password).decode()
            setattr(user, "hashed_password", hashed_password)
            setattr(user, "reset_token", None)
        except (NoResultFound, AssertionError):
            raise ValueError
