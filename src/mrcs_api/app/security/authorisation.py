#!/usr/bin/env python3

"""
Created on 18 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
"""

from typing import Annotated

from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, SecurityScopes
from jwt import InvalidTokenError
from pydantic import ValidationError

from mrcs_api.exceptions import Validation401Exception, InvalidCredentials400Exception, Scope401Exception
from mrcs_api.models.user import APIUser
from mrcs_api.security.scope import Scope, ScopeDescription

from mrcs_core.admin.user.user import User
from mrcs_core.security.token import TokenData


# --------------------------------------------------------------------------------------------------------------------

async def session_user(required: SecurityScopes, encoded_token: EncodedToken) -> APIUser:
    try:
        token = TokenData.decode(encoded_token)
    except (InvalidTokenError, ValidationError, ValueError):
        raise Validation401Exception(required.scope_str)

    user = APIUser.find(token.sub)
    if not user:
        raise InvalidCredentials400Exception()

    # TODO: check if user is enabled - use isInSession=false to log out?
    # TODO: (temporary) check if token scopes == user.scopes

    if not set(required.scopes).issubset(user.scopes()):
        raise Scope401Exception(f'required:{required.scopes} user:{user.scopes}')

    return user


# --------------------------------------------------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='session',
    scopes=ScopeDescription.as_dict(),
)

EncodedToken = Annotated[str, Depends(oauth2_scheme)]

PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]

# --------------------------------------------------------------------------------------------------------------------

AuthorisedAdmin = Annotated[User, Security(session_user, scopes=[Scope.MANAGE_USER_ACCOUNTS])]
AuthorisedDesigner = Annotated[User, Security(session_user, scopes=[Scope.ALTER_LAYOUT])]
AuthorisedOperator = Annotated[User, Security(session_user, scopes=[Scope.OPERATE_EQUIPMENT])]
AuthorisedObserver = Annotated[User, Security(session_user, scopes=[Scope.OBSERVE])]

AuthorisedUser = Annotated[User, Security(session_user, scopes=[])]
