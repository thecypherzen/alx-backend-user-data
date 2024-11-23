#!/usr/bin/env python3
"""End-to-End Integration test
"""

import requests


base_url = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Tests user registration
    """
    res = requests.post(f"{base_url}/users",
                        data={"email": email,
                              "password": password})
    try:
        assert res.status_code == 200 and \
            res.json() == {"email": f"{email}",
                           "message": "user created"}
    except AssertionError:
        res.status_code == 400 and \
            res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test Login with wrong password
    """
    res = requests.post(f"{base_url}/sessions",
                        data={"email": email,
                              "password": password})
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with correct credentials
    """
    res = requests.post(f"{base_url}/sessions",
                        data={"email": email,
                              "password": password})
    assert res.status_code == 200
    assert res.json() == {"email": email,
                          "message": "logged in"}
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test profile fetch for an unlogged in user
    """
    res = requests.get(f"{base_url}/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile fetch for logged in user
    """
    res = requests.get(f"{base_url}/profile",
                       cookies={"session_id": session_id})
    assert res.status_code == 200
    assert res.headers.get("Content-Type") == "application/json"
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Test logging out a logged in user
    """
    res = requests.delete(f"{base_url}/sessions",
                          cookies={"session_id": session_id})
    try:
        assert res.status_code == 403
    except AssertionError:
        assert len(res.history) == 1
        assert res.history[0].headers.get("Location") == \
            "http://0.0.0.0:5000/"
        assert res.history[0].status_code == 302


def reset_password_token(email: str) -> str:
    """Tests reset password route
   """
    res = requests.post(f"{base_url}/reset_password",
                        data={"email": email})
    try:
        assert res.headers.get("Content-Type") == "application/json"
        payload = res.json()
        assert payload.get("email") == email
        assert "reset_token" in payload
        return payload.get("reset_token")
    except AssertionError:
        assert res.status_code == 403


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """Test password update
    """
    res = requests.put(f"{base_url}/reset_password",
                       data={"email": email,
                             "reset_token": reset_token,
                             "new_password": new_password})
    try:
        assert res.status_code == 200
        assert res.headers.get("Content-Type") == "application/json"
        assert res.json() == {"email": email,
                              "message": "Password updated"}
    except AssertionError:
        assert res.status_code == 403


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
