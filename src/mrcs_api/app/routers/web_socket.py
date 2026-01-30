"""
Created on 9 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)

http://bruno.local:8000/ws

General-purpose web socket

https://fastapi.tiangolo.com/advanced/websockets/#await-for-messages-and-send-messages
https://betterstack.com/community/guides/scaling-python/fastapi-websockets/
"""

import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from mrcs_api.app.internal.tags import Tags

from mrcs_control.sys.environment import Environment

from mrcs_core.sys.host import Host
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': web_socket', level=env.log_level)
logger = Logging.getLogger()

logger.info(f'starting')

router = APIRouter(prefix='/ws', tags=[Tags.WebSockets])


# --------------------------------------------------------------------------------------------------------------------

@router.get('')
async def get():
    with open(os.path.join(os.path.dirname(__file__), 'public', 'test_client.html')) as f:
        html = f.read()

    hostname = Host.name()
    logger.info(f'hostname:{hostname}')

    return HTMLResponse(html.replace('XXX.XXX.XXX.XXX', hostname))
