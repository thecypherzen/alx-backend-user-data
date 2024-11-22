#!/usr/bin/env python3
"""Flask Application"""
from auth import Auth
from flask import (
    abort, Flask, json,
    jsonify, request, redirect,
    Response, url_for
)


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def index():
    """GET: /
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """POST /sessions
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    msg = json.dumps({"email": f"{email}", "message": "logged in"})
    response = Response(msg, content_type="application/json")
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """DELETE /logout

    Logs user out of application
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("index"))


@app.route("/profile", strict_slashes=False)
def profile():
    """GET /profile

    Gets a user's profile
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST: /users
    Creates and Adds a new user if possible
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}",
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
