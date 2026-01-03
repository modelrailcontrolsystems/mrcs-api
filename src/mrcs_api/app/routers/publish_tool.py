"""
Created on 27 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/tst/publish

Test publisher tool (TST) API
"""

from fastapi import APIRouter

from mrcs_api.app.internal.tags import Tags
from mrcs_api.app.security.authorisation import AuthorisedOperator
from mrcs_api.exceptions import BadRequest400Exception, NotAcceptable406Exception
from mrcs_api.models.message import APIMessage, MessageModel

from mrcs_control.messaging.mqclient import Publisher
from mrcs_control.sys.environment import Environment

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


# --------------------------------------------------------------------------------------------------------------------

@router.post('/tst/publish', status_code=201, tags=[Tags.Messages])
async def publish(user: AuthorisedOperator, payload: MessageModel):
    logger.info(f'publish - user:{user.uid} payload:{payload}')

    try:
        message = APIMessage.construct_from_payload(payload)
    except ValueError as ex:
        raise BadRequest400Exception(f'publish: {ex}')

    if not message:
        raise NotAcceptable406Exception('publish: malformed payload')

    publisher.publish(message)
