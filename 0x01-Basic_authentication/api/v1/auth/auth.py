#!/usr/bin/env python3
"""This module defines the class `Auth`"""

from flask import request
from typing import List, TypeVar, Union


class Auth:
    """This class provides methods to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """TODO: Implement later"""
        return False

    def authorization_header(self, request=None) -> Union[str, None]:
        """TODO: Implement later"""
        pass

    def current_user(self, request=None) -> TypeVar('User'): # type: ignore
        """TODO: Implement later"""
        pass
