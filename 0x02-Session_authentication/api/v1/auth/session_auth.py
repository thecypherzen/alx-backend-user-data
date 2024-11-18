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

        Returns:
           - None if user_id is None or not a string
           - new session id
        """
        if not user_id or not isinstance(user_id, str):
            return None

        from uuid import uuid4
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def destroy_session(self, request=None):
        """Destroy session on logout
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Fetches a user_id based on session_id

        Returns:
           - None if session_id is None or not a string
           - the user_id for given session_id as contained in
             the <user_id_by_session_id> dictionary
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Fetches user instance from cookie value
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        from models.user import User
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
