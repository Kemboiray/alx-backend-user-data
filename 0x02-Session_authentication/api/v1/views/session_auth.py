#!/usr/bin/env python3
"""This module defines `Flask` views handling session authentication"""

from flask import abort, jsonify, request
import os
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_handler():
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
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            SESSION_NAME = os.getenv("SESSION_NAME")
            res = jsonify(user.to_json())
            res.set_cookie(SESSION_NAME, session_id)
            return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=["DELETE"],
                 strict_slashes=False)
def logout_handler():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - Empty JSON
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
