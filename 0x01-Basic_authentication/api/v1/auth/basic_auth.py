#!/usr/bin/env python3
"""Module defining BasicAuth
"""

from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication class

    Empty for now
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Bearer from Authentication header

        Returns:
           - None if authorization_header is None
           - None if authorization_header is not a string
           - None if authorization_header doesn’t start by
             Basic (with a space at the end)
           - Otherwise the base64 encoding of value after
             Basic (after the space)
           - Assume authorization_header contains only one Basic
        """
        import re
        if any([not authorization_header,
                not isinstance(authorization_header, str)]):
            return None
        match = re.match(r"Basic .+", authorization_header)
        if not match:
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a base64 string to utf-8

        Returns:
           - None if base64_authorization_header is None
           - None if base64_authorization_header is not a string
           - None if base64_authorization_header is not a valid
           - Otherwise:
             - the decoded value as UTF8 string using decode('utf-8')
        """
        if any([not base64_authorization_header,
                not isinstance(base64_authorization_header, str)]):
            return None
        from base64 import b64decode as decode
        try:
            res = str(decode(base64_authorization_header), "utf=8")
            return res
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) \
            -> (str, str):
        """Extracts user credentials - email and password from
        authorization header

        Returns:
           - None, None if decoded_base64_authorization_header is None
           - None, None if decoded_base64_authorization_header
             is not a string
           - None, None if decoded_base64_authorization_header
             doesn’t contain ':'
           - the user email and the user password otherwise
           - assumes there would be only one ':' in string
        """
        if any([not decoded_base64_authorization_header,
                not isinstance(decoded_base64_authorization_header,
                               str)]):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(":")
        return credentials[0], credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """retrieve s user object based on credentials

        Returns:
           - None if user_email is None or not a string
           - None if user_pwd is None or not a string
           - None if the database (file) doesn’t contain any User
             instance with email equal to user_email, using the class
             method search of the User to lookup the list of
             users based on their email.
           - None if user_pwd is not the password of the User instance
             found using the method is_valid_password of User
        """
        if any([not user_email, not isinstance(user_email, str),
               not user_pwd, not isinstance(user_pwd, str)]):
            return None
        from models.user import User
        # check if db is not empty
        try:
            count = User.count()
            if not count:
                return None
        except Exception:
            return None
        # fetch user with matching email and verify iff one
        # user matches email
        user = User.search(attributes={"email": user_email})
        if not user or len(user) > 1 or \
                not isinstance(user[0], User):
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]
