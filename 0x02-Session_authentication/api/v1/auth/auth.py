#!/usr/bin/env python3
"""This module defines the class `Auth`"""

import typing as t
from flask.app import os


class Auth:
    """This class provides methods to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: t.List[str]) -> bool:
        """Return True if authentication is required for `path`"""
        if path is None or not excluded_paths:
            return True
        return not path.rstrip("/") in [i.rstrip("/") for i in excluded_paths]

    def authorization_header(self,
                             request: t.Any = None) -> t.Union[str, None]:
        """
        Return the value of the `Authorization` header or `None` if missing
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None):
        """TODO: Implement later"""
        pass

    def session_cookie(self, request=None) -> t.Union[str, None]:
        """Return the value of the `SESSION_NAME` cookie or `None` if missing
        """
        if request is not None:
            SESSION_NAME = os.getenv("SESSION_NAME")
            return request.cookies.get(SESSION_NAME)
