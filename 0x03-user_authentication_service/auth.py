#!/usr/bin/env python3
"""This module defines `_hash_password`"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Return a salted, hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
