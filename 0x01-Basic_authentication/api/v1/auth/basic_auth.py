#!/usr/bin/env python3
"""Module defining BasicAuth
"""

from api.v1.auth.auth import Auth


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
            return None
        if ":" not in decoded_base64_authorization_header:
            return None
        credentials = decoded_base64_authorization_header.split(":")
        return credentials[0], credentials[1]
