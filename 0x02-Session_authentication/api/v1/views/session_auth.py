#!/usr/bin/env python3
"""This module defines `Flask` views handling session authentication"""

from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_handler():
    email = request.form.get("email", None)
    if email is None:
        return jsonify('{ "error": "email missing" }'), 400
    password = request.form.get("password", None)
    if password is None:
        return jsonify('{ "error": "password missing" }'), 400
    users = User.search({"email": email})
    if not users:
        return jsonify('{"error": "no user found for this email"}')
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth

