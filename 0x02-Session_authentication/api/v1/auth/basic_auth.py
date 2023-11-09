#!/usr/bin/env python3
"""This module defines the class `BasicAuth`"""
from api.v1.auth.auth import Auth
from base64 import b64decode
# from flask import request as flask_request
from models.user import User
from typing import Tuple, Union
import binascii


class BasicAuth(Auth):
    """This class inherits from `Auth`"""

    def extract_base64_authorization_header(
            self, authorization_header: Union[str, None]) -> Union[str, None]:
        """Return the `Base64` part of the Authorization header"""
        if not isinstance(authorization_header, str):
            return None
        return authorization_header.split(
            " ")[1] or None if authorization_header.startswith(
                "Basic ") else None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: Union[str, None]) -> Union[str, None]:
        """Return the decoded value of a `Base64` string"""
        try:
            return b64decode(base64_authorization_header,
                             validate=True).decode("utf-8")
        except (binascii.Error, TypeError, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: Union[str, None]
    ) -> Union[Tuple[str, ...], Tuple[None, None]]:
        """Return user email and password from a `Base64` decoded value"""
        if isinstance(decoded_base64_authorization_header,
                      str) and ":" in decoded_base64_authorization_header:
            return tuple(decoded_base64_authorization_header.split(":"))
        return (None, None)

    def user_object_from_credentials(
            self, user_email: Union[str, None],
            user_pwd: Union[str, None]) -> Union[User, None]:
        """Return the `User` instance based on email and password"""
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return
        try:
            users = User.search({"email": user_email})
        except KeyError:
            return
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> Union[User, None]:
        """Overload `Auth` and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        base64_auth_header_de = self.decode_base64_authorization_header(
            base64_auth_header)
        user_credentials = self.extract_user_credentials(
            base64_auth_header_de)
        return self.user_object_from_credentials(*user_credentials)
