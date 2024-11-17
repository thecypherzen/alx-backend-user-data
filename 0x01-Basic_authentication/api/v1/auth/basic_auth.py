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
