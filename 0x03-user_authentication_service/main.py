#!/usr/bin/env python3
"""
This module defines functions to test the user authentication service.
"""
import requests

BASE_URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str):
    """Test user registration functionality."""
    url = BASE_URL + "/users"
    response = requests.post(url, dict(email=email, password=password))
    assert response.status_code == 200, str(
        response.status_code) + " " + response.reason
    expected = {"email": email, "message": "user created"}
    assert response.json() == expected, f"{response.json()} != {expected}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Test for correct response in case of wrong password."""
    url = BASE_URL + "/sessions"
    response = requests.post(url, dict(email=email, password=password))
    assert response.status_code == 401, f"{response.status_code} != 401"


def log_in(email: str, password: str) -> str:
    """Test login functionality"""
    url = BASE_URL + "/sessions"
    response = requests.post(url, dict(email=email, password=password))
    assert response.status_code == 200, str(
        response.status_code) + " " + response.reason
    expected = dict(email=email, message="logged in")
    assert response.json() == expected, f"{response.json()} != {expected}"
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "session_id cookie is not set"
    return session_id


def profile_unlogged() -> None:
    """Test access to `/profile` endpoint when unlogged."""
    url = BASE_URL + "/profile"
    response = requests.get(url)
    assert response.status_code == 403, f"{response.status_code} != 403"


def profile_logged(session_id: str) -> None:
    """Test access to `/profile` endpoint when logged in."""
    url = BASE_URL + "/profile"
    response = requests.get(url, dict(session_id=session_id))
    assert response.status_code == 200, str(
        response.status_code) + " " + response.reason
    expected = {"email": EMAIL}
    assert response.json() == expected, f"{response.json()} != {expected}"


def log_out(session_id: str) -> None:
    """Test logout functionality."""
    url = BASE_URL + "/sessions"
    response = requests.delete(url, dict(session_id=session_id))
    assert response.status_code == 200, str(
        response.status_code) + " " + response.reason
    expected = {"message": "Bienvenue"}
    assert response.json() == expected, f"{response.json()} != {expected}"


def reset_password_token(email: str) -> str:
    """Test reset password token functionality."""
    url = BASE_URL + "/reset_password"
    response = requests.post(url, dict(email=email))
    assert response.status_code == 200, str(
        response.status_code) + " " + response.reason
    reset_token = response.json().get("reset_token")
    assert isinstance(reset_token, str) and len(reset_token) == 72, \
        "`reset_token` is not a string or has not the expected length (72)"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update password functionality."""
    url = BASE_URL + "/reset_password"
    response = requests.put(
        url,
        dict(email=email, reset_token=reset_token, new_password=new_password))
    expected = {"email": email, "message": "Password updated"}
    assert response.status_code == 200, str(
        response.status_code) + " " + response.reason
    assert response.json() == expected, f"{response.json()} != {expected}"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
