#!/usr/bin/env python3
"""API Authentication Module
"""

from flask import request
from typing import List, TypeVar
from os import environ


class Auth:
    """Authentication Class Definition
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """Verifies if a path requires authentication
        Returns:
           - True if authentication is required
           - False otherwise
        """
        if path is None or not isinstance(path, str) \
           or not excluded_paths:
            return True
        status = True
        for expath in excluded_paths:
            if expath[-1] == '*':
                if expath[0:-1] == path[0:len(expath) - 1]:
                    status = False
                    break
            else:
                if path + '/' == expath:
                    status = False
                    break
            return True
        return status

    def authorization_header(self, request=None) -> str:
        """Sets authorization header in a request

        Params:
           request(obj:flask.request): the current request object
        Returns:
           None
        """
        if not request:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the currently logged in user if there is
        one for the current inbound `request` or saves the
        requesting user's data.

        Params:
           request(obj:flask.request): the current request object

        Returns:
           - the currently logged in user if any
           - the requesting user
        """
        return None

    def session_cookie(self, request=None):
        """Fetches a cookie from request

        Returns:
           - None if request is None
           - value of cookied named '_my_session_id' from 'request'.
             the name of the cookie is defined by the environment
             variable SESSION_NAME
        """
        if not request:
            return None
        return request.cookies.get(environ.get('SESSION_NAME'))
