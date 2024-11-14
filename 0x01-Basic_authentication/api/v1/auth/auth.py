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
        return False

    def authorization_header(self, request=None) -> str:
        """Sets authorization header in a request

        Params:
           request(obj:flask.request): the current request object
        Returns:
           None
        """
        return None

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
