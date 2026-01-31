#!/usr/bin/env python3

"""
Created on 27 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/
http://127.0.0.1:8000/docs

MRCS_LOG_NAME=mrcs_fastapi; MRCS_LOG_LEVEL=20; MRCS_OPS_MODE=TEST; fastapi dev src/mrcs_web/app/main.py

https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure
https://github.com/fastapi/fastapi/discussions/6055
https://fastapi.tiangolo.com/advanced/events/#lifespan
https://dev.to/leapcell/mastering-python-async-io-with-fastapi-13e8
"""

import socket
from contextlib import asynccontextmanager

from fastapi import FastAPI  # Depends,

from mrcs_api.app.routers import (message_logger, publish_tool, session_controller, time_controller, user_admin,
                                  web_socket)

from mrcs_api.app.routers.time_controller import time_controller_node

from mrcs_control.db.db_client import DbClient
from mrcs_control.sys.environment import Environment

from mrcs_core.sys.logging import Logging

# from .dependencies import get_query_token, get_token_header
# from .internal import admin


# --------------------------------------------------------------------------------------------------------------------

__TITLE = 'MRCS Controller API'
__SUMMARY = 'Provides an interface to MRCS command operations for the MRCS Web User Interface and CLI.'

# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()
Logging.config(env.log_name + ': main', level=env.log_level)

logger = Logging.getLogger()
logger.info(f'starting: {env}')

DbClient.set_client_db_mode(env.ops_mode.value.db_mode)

hostname = socket.gethostname()
logger.info(f'hostname:{hostname}')


# --------------------------------------------------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info('lifespan: part1 - start')

    time_controller_node.connect()
    await time_controller_node.connection_is_available()

    logger.info('lifespan: part1 - end')
    yield

    logger.info('lifespan: part2')


# --------------------------------------------------------------------------------------------------------------------

app = FastAPI(title=__TITLE, summary=__SUMMARY, lifespan=lifespan)
# , lifespan=lifespan, dependencies=[Depends(get_query_token)]

app.include_router(message_logger.router)
app.include_router(publish_tool.router)
app.include_router(session_controller.router)
app.include_router(time_controller.router)
app.include_router(user_admin.router)
app.include_router(web_socket.router)

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get('/')
async def root():
    return {"id": "MRCS API"}
