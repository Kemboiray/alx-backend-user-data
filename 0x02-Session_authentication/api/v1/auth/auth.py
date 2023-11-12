#!/usr/bin/env python3
"""This module defines the class `Auth`"""

# from flask import request
import typing as t
import os

SESSION_NAME = os.getenv("SESSION_NAME")


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

    def current_user(self, request=None) -> t.TypeVar('User'):  # type: ignore
        """TODO: Implement later"""
        pass

    def session_cookie(self, request=None) -> t.Union[str, None]:
        if request is not None:
            return request.cookies.get(SESSION_NAME)
