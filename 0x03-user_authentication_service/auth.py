#!/usr/bin/env python3
"""Authentication Module
"""
from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """Generates a hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

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
