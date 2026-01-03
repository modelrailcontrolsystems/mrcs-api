"""
Created on 13 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

Authentication and authorisation exceptions
"""

from fastapi import HTTPException
from fastapi import status


# ----------------------------------------------------------------------------------------------------------------

class InvalidCredentials400Exception(HTTPException):
    """
    Security exception: invalid credentials
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='incorrect username or password',
        )


# ----------------------------------------------------------------------------------------------------------------

class Validation401Exception(HTTPException):
    """
     Security ValidationException: no username or no user
    """

    def __init__(self, authenticate_value: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='could not validate credentials',
            headers={'WWW-Authenticate': authenticate_value}
        )


# ----------------------------------------------------------------------------------------------------------------

class Scope401Exception(HTTPException):
    """
    Security ScopeException: user or token scopes do not include path scope
    """

    def __init__(self, authenticate_value: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not enough permissions',
            headers={'WWW-Authenticate': authenticate_value}
        )


# ----------------------------------------------------------------------------------------------------------------

class InactiveUser401Exception(HTTPException):
    """
    Security exception: user is not enabled
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='inactive user',
        )
