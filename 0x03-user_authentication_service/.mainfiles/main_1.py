#!/usr/bin/env python3

"""
Main file
"""

from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

user3 = my_db.get_user(user_2.id)
print(getattr(user3, "id", None))
print(getattr(user3, "email", None))
print(getattr(user3, "hashed_password", None))
print(getattr(user3, "session_id", None))
print(getattr(user3, "reset_token", None ))
