#!/usr/bin/env python3
"""This module defines `Flask` views handling session authentication"""

from flask import jsonify, request, Response
from flask.app import os
from api.v1.views import app_views
from models.user import User
import typing as t


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_handler() -> t.Tuple[Response, int]:
    """ POST /api/v1/auth_session/login
    Return:
      - User instance JSON represented
    """
    email = request.form.get("email", None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password", None)
    if password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"})
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            SESSION_NAME = os.getenv("SESSION_NAME")
            res = jsonify(user.to_json())
            res.set_cookie(SESSION_NAME, session_id)
            return res
    return jsonify({"error": "wrong password"}), 401
