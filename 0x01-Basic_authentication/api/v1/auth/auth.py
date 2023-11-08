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
        return not path.rstrip("/") in [i.rstrip("/") for i in excluded_paths]

    def authorization_header(self, request=None) -> Union[str, None]:
        """TODO: Implement later"""
        pass

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """TODO: Implement later"""
        pass
