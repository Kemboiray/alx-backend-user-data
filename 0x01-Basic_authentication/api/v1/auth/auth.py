#!/usr/bin/env python3
"""This module defines the class `Auth`"""

from flask import request
from typing import List, TypeVar, Union


class Auth:
    """This class provides methods to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return True if authentication is required for `path`"""
        if path is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                if path.startswith(excluded_path[:-1]):
                    return False
        return not path.rstrip("/") in [i.rstrip("/") for i in excluded_paths]

    def authorization_header(self, request=None) -> Union[str, None]:
        """
        Return the value of the `Authorization` header or `None` if missing
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """TODO: Implement later"""
        pass
