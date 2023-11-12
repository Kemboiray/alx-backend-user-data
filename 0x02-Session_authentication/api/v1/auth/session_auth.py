#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module defines the `SessionAuth` class"""

import typing as t
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """This class inherits from `Auth`"""

    user_id_by_session_id = {}

    def create_session(self, user_id: t.Union[str,
                                              None]) -> t.Union[str, None]:
        """This method creates a Session ID for a user_id"""
        if isinstance(user_id, str):
            self.session_id = str(uuid4())
            SessionAuth.user_id_by_session_id[self.session_id] = user_id
            return self.session_id
