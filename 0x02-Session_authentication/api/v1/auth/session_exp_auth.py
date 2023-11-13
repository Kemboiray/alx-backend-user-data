#!/usr/bin/env python3
"""
This module defines `SessionExpAuth`, a subclass of `SessionAuth`.
`SessionExpAuth` adds an expiration date to a Session ID.
"""
import os
import typing as t
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime as d, timedelta as td

try:
    SESSION_DURATION = int(os.getenv("SESSION_DURATION", 0))
except ValueError:
    SESSION_DURATION = 0


class SessionExpAuth(SessionAuth):
    """
    This class adds an expiration date to a Session ID defined in
    `SessionAuth.`
    """

    def __init__(self) -> None:
        """Class constructor method"""
        self.session_duration = SESSION_DURATION

    def create_session(self,
                       user_id: t.Union[str,
                                        None] = None) -> t.Union[str, None]:
        """
        Create a Session with an expiry.

        Oveloads `SessionAuth.create_session`.
        """
        session_id = super().create_session(user_id)
        if session_id is not None:
            self.user_id_by_session_id[session_id] = dict(user_id=user_id,
                                                          created_at=str(
                                                              d.now()))
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return a User ID corresponding to a Session ID.

        Overloads `SessionAuth.user_id_for_session_id.`
        """
        session_dict = self.user_id_by_session_id.get(session_id)
        if isinstance(session_dict, dict) and "created_at" in session_dict:
            age = d.now() - d.fromisoformat(session_dict["created_at"])
            if self.session_duration <= 0 or age < td(self.session_duration):
                return session_dict.get("user_id")
