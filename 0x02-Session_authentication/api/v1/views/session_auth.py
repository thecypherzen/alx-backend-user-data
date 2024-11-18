#!/usr/bin/env python3
"""API views for session authentication
"""

from api.v1.views import app_views
from flask import json, request, Response
from models.user import User
from os import environ


@app_views.route('/auth_session/login',
                 methods=["POST"], strict_slashes=False)
def session_auth():
    """Handle session authentication
    """
    email, password = [request.form.get("email"),
                       request.form.get("password")]
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search(attributes={"email": email})[0]
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = Response(json.dumps(user.to_json()),
                        content_type="application/json")
    response.set_cookie(environ.get("SESSION_NAME"), session_id)
    return response
