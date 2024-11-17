#!/usr/bin/env python3
"""API Authentication Module
"""

from flask import request
from typing import List, TypeVar


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
        print(path, excluded_paths)
        if path is None or not isinstance(path, str) \
           or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        print("final path:", path)
        if path not in excluded_paths:
            return True
        return False

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
