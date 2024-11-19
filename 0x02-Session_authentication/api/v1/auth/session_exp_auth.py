#!/usr/bin/env python3
"""Session Expiration Definition Module
"""

from api.v1.auth.session_auth import SessionAuth
from os import environ


class SessionExpAuth(SessionAuth):
    """A session expiration definition class
    """
    user_id_by_session_id = {}

    def __init__(self):
        """Initialises class
        """
        env_value = environ.get("SESSION_DURATION")
        duration = 0
        if env_value:
            try:
                duration = int(env_value)
            except Exception:
                pass
        self.session_duration = duration

    def create_session(self, user_id=None):
        """Creates a session instance
        """
        from datetime import datetime

        session_id = super().create_session(user_id)
        if not session_id:
            return None
        SessionExpAuth.user_id_by_session_id[session_id] = \
            {"session dictionary": {"user_id": user_id,
                                    "created_at": datetime.now()}
             }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Fetches a user_id associated with session_id
        """
        from datetime import datetime, timedelta

        if not session_id:
            return None
        if session_id not in SessionExpAuth.user_id_by_session_id:
            return None
        session_dic = SessionExpAuth.user_id_by_session_id[session_id]\
            .get("session dictionary")
        if self.session_duration <= 0:
            return session_dic["user_id"]
        if "created_at" not in session_dic:
            return None
        created_at = session_dic["created_at"]
        delta = created_at + timedelta(seconds=self.session_duration)
        if delta < datetime.now():
            return None
        return session_dic["user_id"]
