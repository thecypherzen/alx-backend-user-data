#!/usr/bin/env python3
"""Utility Methods and Functions
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Generates a hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
