#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module defines the `SessionAuth` class"""

import typing as t
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """This class inherits from `Auth`"""

    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: t.Union[str,
                                              None]) -> t.Union[str, None]:
        """Create a Session ID for a user_id"""
        if isinstance(user_id, str):
            self.session_id = str(uuid4())
            SessionAuth.user_id_by_session_id[self.session_id] = user_id
            return self.session_id

    def user_id_for_session_id(
            self, session_id: t.Union[str, None]) -> t.Union[str, None]:
        """Return a User ID corresponding to a Session ID if it exists."""
        if isinstance(session_id, str):
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> t.Union[User, None]:
        """Return an instance of `User` based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if isinstance(user_id, str):
            return User.get(user_id)
