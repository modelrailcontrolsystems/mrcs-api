"""
Created on 27 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

Message logger (MLG) API

http://127.0.0.1:8000/mlg/latest

https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure
"""

from typing import List

from fastapi import APIRouter

from mrcs_api.app.internal.tags import Tags
from mrcs_api.app.security.authorised import AuthorisedObserver
from mrcs_api.models.message import MessageRecordModel

from mrcs_core.data.json import JSONify
from mrcs_core.operations.recorder.message_recorder import MessageRecorder
from mrcs_core.sys.environment import Environment
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': message_logger', level=env.log_level)
logger = Logging.getLogger()

logger.info(f'starting')

router = APIRouter()

recorder = MessageRecorder.construct(env.ops_mode)


# --------------------------------------------------------------------------------------------------------------------

@router.get('/mlg/latest', tags=[Tags.Messages])
async def latest_messages(user: AuthorisedObserver, limit: int = 10) -> List[MessageRecordModel]:
    logger.info(f'latest_messages - user:{user.uid} limit:{limit}')
    records = list(recorder.find_latest(limit))

    return JSONify.as_jdict(records)
