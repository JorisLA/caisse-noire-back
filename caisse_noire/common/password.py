"""
Password-related utilities
This is an utility class (not supposed to have instances)
"""

import re
import unicodedata
from collections import Counter
from typing import Optional

from app import bcrypt


class Passwords(object):
    """
    Password utilities
    """
    BC_PATTERN = re.compile(r'^\$2a\$\d\d\$[./a-zA-Z0-9]{53}$')

    @staticmethod
    def hash_password(password: str, current_hash: Optional[str] = None) -> str:
        """
        Create a hash of a password using bcrypt.

        Args:
            password (str): Password to hash
            current_hash (str): The current hash, if any

        Returns:
            str: Generated hash
        """
        return password if current_hash == 'bcrypt' else \
            bcrypt.generate_password_hash(
                password,
                14
            ).decode('utf-8')

    @staticmethod
    def _is_clear_password_valid(password: str) -> bool:
        """
        Check an unicode password validity. To be valid,
        it must meet all the following requirements:
            - At least 8 characters
        Args:
            password (str): Password to check

        Returns:
            bool: True if the password is valid, False otherwise
        """
        if password is None:
            return False
        c = Counter([unicodedata.category(c) for c in password])
        rules = [
            # must be at least 8 characters
            lambda s: len(s) >= 8,
        ]
        return all(rule(password) for rule in rules)

    @staticmethod
    def _is_bcrypt_hash_valid(hashed_pass: str) -> bool:
        """
        Check if a bcrypt hashed password is valid
            - Size is 60
            - Uses $2a$ seeds
            - Between 12 and 31 rounds
        Args:
            hashed_pass(str or bytes): The hash to be checked

        Returns:
            bool: True if valid, False otherwise
        """
        rules = [
            lambda s: type(s) is str,
            lambda s: Passwords.BC_PATTERN.fullmatch(s),
            lambda s: '12' <= s[4:6] <= '31',
        ]
        return all(rule(hashed_pass) for rule in rules)

    @staticmethod
    def is_password_valid(password: str, password_hash: Optional[str] = None) -> bool:
        """
        Check an eventually hashed password validity

        Args:
            password (str): Password to be checked
            password_hash (str): The password hash, or None

        Returns:
            bool: True if the password is valid, False otherwise
        """

        if not password_hash:
            return Passwords._is_clear_password_valid(password)

        if password_hash == 'bcrypt':
            return Passwords._is_bcrypt_hash_valid(password)

        return False
