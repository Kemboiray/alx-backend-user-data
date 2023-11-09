#!/usr/bin/env python3
"""This module defines the class `BasicAuth`"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Union
import binascii


class BasicAuth(Auth):
    """This class inherits from `Auth`"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> Union[str, None]:
        """Return the Base64 part of the Authorization header"""
        if not isinstance(authorization_header, str):
            return None
        return authorization_header.split(
            " ")[1] or None if authorization_header.startswith(
                "Basic ") else None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> Union[str, None]:
        """Return the decoded value of a Base64 string"""
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = b64decode(base64_authorization_header,
                                validate=True).decode("utf-8")
        except binascii.Error:
            return None
        return decoded
