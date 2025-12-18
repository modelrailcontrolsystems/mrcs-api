#!/usr/bin/env python3

"""
Created on 18 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
"""

from typing import Annotated

from fastapi import Security

from mrcs_api.app.security.scope import Scope
from mrcs_api.app.routers.session_controller import session_user
from mrcs_core.admin.user.user import User


# --------------------------------------------------------------------------------------------------------------------

AuthorisedAdmin = Annotated[User, Security(session_user, scopes=[Scope.MANAGE_USER_ACCOUNTS])]
AuthorisedDesigner = Annotated[User, Security(session_user, scopes=[Scope.ALTER_LAYOUT])]
AuthorisedOperator = Annotated[User, Security(session_user, scopes=[Scope.OPERATE_EQUIPMENT])]
AuthorisedObserver = Annotated[User, Security(session_user, scopes=[Scope.OBSERVE])]

AuthorisedUser = Annotated[User, Security(session_user, scopes=[])]
