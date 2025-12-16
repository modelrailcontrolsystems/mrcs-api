"""
Created on 27 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

Test publisher tool (TST) API
"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Security

from mrcs_api.app.routers.session_controller import session_user
from mrcs_api.models.message import APIMessage, MessageModel

from mrcs_core.admin.user.user import User
from mrcs_core.messaging.mqclient import Publisher
from mrcs_core.sys.environment import Environment
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': publish_tool', level=env.log_level)
logger = Logging.getLogger()

logger.info(f'starting')

router = APIRouter()

publisher = Publisher.construct_pub(env.ops_mode.value.mq_mode)
publisher.connect()
logger.info(f'publisher:{publisher}')

AuthorizedUser = Annotated[User, Security(session_user, scopes=['OPERATE'])]


# --------------------------------------------------------------------------------------------------------------------

@router.post('/tst/publish', tags=['messages'])
async def publish(user: AuthorizedUser, payload: MessageModel):
    logger.info(f'publish - user:{user} payload:{payload}')

    try:
        message = APIMessage.construct_from_payload(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=f'publish: {ex}')

    if not message:
        raise HTTPException(status_code=400, detail='publish: malformed payload')

    publisher.publish(message)
