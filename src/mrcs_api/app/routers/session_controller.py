"""
Created on 12 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

User session API

https://stackoverflow.com/questions/5868786/what-method-should-i-use-for-a-login-authentication-request
"""

from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from fastapi import APIRouter, Depends
from jwt import InvalidTokenError
from pydantic import ValidationError

from mrcs_api.exceptions import Validation401Exception, Scope401Exception, InvalidCredentials400Exception
from mrcs_api.models.session import Scope
from mrcs_api.models.token import TokenModel, JWT, TokenData

from mrcs_core.admin.user.user import User
from mrcs_core.db.dbclient import DBClient
from mrcs_core.sys.environment import Environment
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': session_controller', level=env.log_level)
logger = Logging.getLogger()

DBClient.set_client_db_mode(env.ops_mode.value.db_mode)

logger.info(f'starting - client_db_mode:{DBClient.client_db_mode()}')

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='session',
    scopes=Scope.as_dict(),
)

router = APIRouter()


# --------------------------------------------------------------------------------------------------------------------

async def session_user(required: SecurityScopes, encoded_token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        token = TokenData.decode(encoded_token)
    except (InvalidTokenError, ValidationError, ValueError):
        raise Validation401Exception(required.scope_str)

    user = User.find(token.sub)
    if not user:
        raise InvalidCredentials400Exception()

    # TODO: check if user is enabled - use enabled=false to log out?

    if not set(required.scopes).issubset(token.scopes):        # TODO: user user's instead of token's scopes?
        raise Scope401Exception(f'required:{required.scopes} presented:{token.scopes}')

    return user


# --------------------------------------------------------------------------------------------------------------------

@router.post('/session', status_code=201, tags=['session'])
async def create(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenModel:
    user = User.log_in(form.username, form.password)
    if not user:
        raise InvalidCredentials400Exception()

    return JWT.construct(user).encode()
