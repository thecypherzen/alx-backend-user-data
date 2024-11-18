#!/usr/bin/env python3
"""Session Authentication Module
"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication Class
    """
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates session_id for user_id
        """
        if not user_id or not isinstance(user_id, str):
            return None

        from uuid import uuid4
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
