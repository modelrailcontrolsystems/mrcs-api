"""
Created on 12 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/session

User session API

https://stackoverflow.com/questions/5868786/what-method-should-i-use-for-a-login-authentication-request
"""

from fastapi import APIRouter

from mrcs_api.app.internal.tags import Tags
from mrcs_api.app.security.authorisation import PasswordRequestForm
from mrcs_api.exceptions import InvalidCredentials400Exception
from mrcs_api.models.user import APIUser
from mrcs_api.security.token import TokenModel, APIJWT

from mrcs_control.db.db_client import DbClient
from mrcs_control.sys.environment import Environment

from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': session_controller', level=env.log_level)
logger = Logging.getLogger()

DbClient.set_client_db_mode(env.ops_mode.value.db_mode)

logger.info(f'starting - client_db_mode:{DbClient.client_db_mode()}')

# TODO: is the DbClient needed here?
router = APIRouter()


# --------------------------------------------------------------------------------------------------------------------

@router.post('/session', status_code=201, tags=[Tags.Session])
async def create(form: PasswordRequestForm) -> TokenModel:
    user = APIUser.log_in(form.username, form.password)
    if not user:
        raise InvalidCredentials400Exception()

    return APIJWT.construct(user).encode()
