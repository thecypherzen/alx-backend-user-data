#!/usr/bin/env python3
"""Session Persisting Module
"""
from models.base import Base


class UserSession(Base):
    """User Session Class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initialises the class
        """
       super().__init(*args, **kwargs)
       self.user_id:str = kwargs.get("user_id")
       self.session_id = kwargs.get("session_id")
