#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Mapping, Optional, TypeVar
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

    def add_user(self, email: str, h_pwd: str) -> User:
        """Adds a user to db"""
        user = User(email=email, hashed_password=h_pwd)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self,
                     **kwargs: Mapping[str, str]) -> Optional[User]:
        """Finds user by keyword args

        Raises:
           - NoResultFound: when no results are found
           - InvalidRequestError: when wrong query arguments are passed
        Returns:
           - The first row found in the users table as filtered by
             the input arguments.
        """
        session = self.__get_session()
        if kwargs is None:
            raise InvalidRequestError()
        return session.query(User).filter_by(**kwargs).one()

    def __get_session(self):
        """Fetches a new session instance from pool
        """
        if self.__session:
            return self.__session
        return self._session
