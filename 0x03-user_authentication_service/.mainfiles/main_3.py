#!/usr/bin/env python3

"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"

user = my_db.add_user(email, hashed_password)
print(user.id)

try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
    try:
        db = DB()
        n_user = db.find_user_by(email=email,
                                 hashed_password="NewPwd")
        print("old: {}\nnew: {}".format(hashed_password,
                                        n_user.hashed_password))
        print(user.hashed_password)
    except InvalidRequestError:
        print("change didn't persist to db")
except ValueError:
    print("Error")
