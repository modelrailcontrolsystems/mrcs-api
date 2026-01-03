"""
Created on 13 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

Authentication and authorisation exceptions
"""

from fastapi import HTTPException
from fastapi import status


# ----------------------------------------------------------------------------------------------------------------

class BadRequest400Exception(HTTPException):
    """
    The server cannot or will not process the request due to an apparent client error.
    """

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class InvalidCredentials400Exception(HTTPException):
    """
    Security exception: invalid credentials.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='incorrect username or password',
        )


# ----------------------------------------------------------------------------------------------------------------

class Validation401Exception(HTTPException):
    """
     Security ValidationException: no username or no user.
    """

    def __init__(self, authenticate_value: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='could not validate credentials',
            headers={'WWW-Authenticate': authenticate_value}
        )


class Scope401Exception(HTTPException):
    """
    Security ScopeException: user or token scopes do not include path scope.
    """

    def __init__(self, authenticate_value: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not enough permissions',
            headers={'WWW-Authenticate': authenticate_value}
        )


class InactiveUser401Exception(HTTPException):
    """
    Security exception: user is not enabled.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='inactive user',
        )


# ----------------------------------------------------------------------------------------------------------------

class NotFound404Exception(HTTPException):
    """
    The requested resource could not be found but may be available in the future.
    """

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


# ----------------------------------------------------------------------------------------------------------------

class NotAcceptable406Exception(HTTPException):
    """
    The requested resource is capable of generating only content not acceptable...
    """

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=detail,
        )


# ----------------------------------------------------------------------------------------------------------------

class Conflict409Exception(HTTPException):
    """
    The request could not be processed because of conflict in the current state of the resource.
    """

    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )
