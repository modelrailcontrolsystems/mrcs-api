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
"""

from fastapi import FastAPI     # Depends,

from mrcs_api.app.routers import message_logger, publish_tool, user_admin

from mrcs_core.db.dbclient import DBClient
from mrcs_core.sys.environment import Environment
from mrcs_core.sys.logging import Logging

# from .dependencies import get_query_token, get_token_header
# from .internal import admin


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()
Logging.config(env.log_name + ': main', level=env.log_level)

logger = Logging.getLogger()
logger.info(f'starting: {env}')

DBClient.set_client_db_mode(env.ops_mode.value.db_mode)


# --------------------------------------------------------------------------------------------------------------------


app = FastAPI()     # dependencies=[Depends(get_query_token)]

app.include_router(message_logger.router)
app.include_router(user_admin.router)
app.include_router(publish_tool.router)

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"id": "MRCS Web"}
