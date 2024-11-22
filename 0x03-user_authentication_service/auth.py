#!/usr/bin/env python3
"""Authentication Module
"""
from db import DB
from user import User
import bcrypt


def _generate_uuid() -> str:
    """Generates a uuid
    """
    from uuid import uuid4

    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """Generates a hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def create_session(self, email: str) -> str:
        """Creates a session instance
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Removes a user from session

        Updates current user's session_id to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token
        """
        from uuid import uuid4

        try:
            user = self._db.find_user_by(email=email)
            token = str(uuid4())
            user.reset_token = token
            return token
        except Exception:
            raise ValueError()

    def get_user_from_session_id(self, session_id: str) -> User:
        """Finds a user by session_id

           Params:
              - session_id(str): the user's session_id

           Returns:
              The User with <session_id> if found else None
        """
        if not session_id or not isinstance(session_id, str):
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def register_user(self, email: str,
                      password: str) -> User:
        """Creates and adds a new user to the db

        Hashes the password with _hash_password, and saves the user
        to the database using self._db

        Params:
           - email(str): the user's email
           - password(str): the user's password

        Raises:
           - ValueError: if a user already exist with the passed email
             - Message: User <user's email> already exists.

        Returns:
           - New User object on success
           - None on failure
        """
        from sqlalchemy.orm.exc import NoResultFound

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if credentials match that of a user

        Params:
           - email(str): the user's email
           - password(str): the user's password
        Returns:
           - True if user by email exist and password matches the user
           - False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except Exception:
            return False
