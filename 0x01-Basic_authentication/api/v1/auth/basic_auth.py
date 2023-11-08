#!/usr/bin/env python3
"""This module defines the class `BasicAuth`"""
from api.v1.auth.auth import Auth
from typing import Union


class BasicAuth(Auth):
    """This class inherits from `Auth`"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> Union[str, None]:
        """Return the Base64 part of the Authorization header"""
        if not isinstance(authorization_header, str):
            return None
        return authorization_header.split(
            " ")[1] if authorization_header.startswith("Basic ") else None
