#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import Mapping
from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to db

        Params:
           - email(str): user email
           - h_pwd(str): user hashed password

        Returns:
           User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self,
                     **kwargs: Mapping[str, str]) -> User:
        """Finds user by keyword args

        Params:
           - kwargs(Obj[str, str]): keyword arguments of attributes
        Raises:
           - NoResultFound: when no results are found
           - InvalidRequestError: when wrong query arguments are passed
        Returns:
           - The first row found in the users table as filtered by
             the input arguments.
        """
        if kwargs is None:
            raise InvalidRequestError
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError()
        user = self._session.query(User).filter_by(**kwargs).one()
        if not user:
            raise NoResultFound
        return user

    def __get_session(self):
        """Fetches a new session instance from pool
        """
        if self.__session:
            return self.__session
        return self._session
