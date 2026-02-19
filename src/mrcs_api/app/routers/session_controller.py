"""
Created on 12 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/session

User session API

https://stackoverflow.com/questions/5868786/what-method-should-i-use-for-a-login-authentication-request
"""

from fastapi import APIRouter, status

from mrcs_api.app.internal.tags import Tags
from mrcs_api.app.security.authorisation import PasswordRequestForm
from mrcs_api.exceptions import InvalidCredentials400Exception
from mrcs_api.models.token import TokenModel
from mrcs_api.models.user import APIUser
from mrcs_api.security.token import APIJWT
from mrcs_api.security.token_timeout import TokenTimeout
from mrcs_control.sys.environment import Environment
from mrcs_core.sys.host import Host
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': session_controller', level=env.log_level)
logger = Logging.getLogger()

timeout = TokenTimeout.load(Host)
logger.info(timeout)

router = APIRouter(prefix='/session', tags=[Tags.Session])


# --------------------------------------------------------------------------------------------------------------------

@router.post('', status_code=status.HTTP_201_CREATED)
async def create(form: PasswordRequestForm) -> TokenModel:
    user = APIUser.log_in(form.username, form.password)
    if not user:
        raise InvalidCredentials400Exception()

    return APIJWT.construct(user, timeout.delta()).encode()
