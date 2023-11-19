#!/usr/bin/env python3
"""
This module defines functions to test the user authentication service.
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str):
    """Test user registration functionality."""
    url = BASE_URL + "/users"
    response = requests.post(url, dict(email=email, password=password))
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test for correct response in case of wrong password."""
    url = BASE_URL + "/sessions"
    response = requests.post(url, dict(email=email, password=password))
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login functionality"""
    url = BASE_URL + "/sessions"
    response = requests.post(url, dict(email=email, password=password))
    assert response.status_code == 200
    assert response.json() == dict(email=email, message="logged in")
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Test access to `/profile` endpoint when unlogged"""
    url = BASE_URL + "/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test access to `/profile` endpoint when logged in."""
    url = BASE_URL + "/profile"
    response = requests.get(url, dict(session_id=session_id))
    assert response.status_code == 200
    assert response.json()


def log_out(session_id: str) -> None:
    pass


def reset_password_token(email: str) -> str:
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    pass


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

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
