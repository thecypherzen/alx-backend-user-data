#!/usr/bin/env python3
"""Session authentication using db Module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session db authentication class
    """

    def create_session(self, user_id=None):
        """creates new session
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        user_session = UserSession(user_id=user_id,
                                   session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves user_id by session_id
        """
        if not session_id or not isinstance(session_id, str):
            return None

        # get UserSession in db if possible
        try:
            user_session = UserSession.search({"session_id": session_id})
            if not user_session:
                return None
        except Exception:
            return None

        user_id = super().user_id_for_session_id(session_id=session_id)
        if not user_id:
            user_session[0].remove()
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """Destroys session"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        if user_session:
            user_session[0].remove(0)
        return True
