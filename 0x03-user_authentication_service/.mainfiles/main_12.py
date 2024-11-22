#!/usr/bin/env python3

from auth import Auth

email = "user@email"
password = "user.password"

auth = Auth()

user = auth.register_user(email, password)
print("user:{} | email:{}".format(user.id, user.email))

user_session = auth.create_session(user.email)
print("session_id:",user_session)

# auth._session.commit()
user2 = auth.get_user_from_session_id(user_session)
if not user2:
    print("User not found")
else:
    print("user1 id: {}, user2 id:{}".format(user.id, user2.id))
