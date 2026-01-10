"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/time

Time API
"""

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from mrcs_api.app.internal.tags import Tags
from mrcs_api.app.internal.web_socket_manager import WebSocketManager
from mrcs_api.app.security.authorisation import AuthorisedOperator
from mrcs_api.exceptions import Conflict409Exception
from mrcs_api.models.time import ClockSetModel, ClockConfModel

from mrcs_control.sys.environment import Environment

from mrcs_core.data.json import JSONify
from mrcs_core.operations.time.clock import Clock
from mrcs_core.operations.time.persistent_iso_datetime import PersistentISODatetime
from mrcs_core.sys.host import Host

from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': time', level=env.log_level)
logger = Logging.getLogger()

logger.info(f'starting')

ws_manager = WebSocketManager(logger)
logger.info(f'ws_manager:{ws_manager}')

router = APIRouter()


# --------------------------------------------------------------------------------------------------------------------

@router.get('/time/now', tags=[Tags.Time])
async def now() -> str:
    logger.info(f'now')

    clock = Clock.load(Host)
    return JSONify.as_jdict(clock.now())


@router.get('/time/conf', tags=[Tags.Time])
async def conf() -> ClockConfModel:
    logger.info(f'conf')

    clock = Clock.load(Host)
    await ws_manager.broadcast(JSONify.as_jdict(clock))

    return JSONify.as_jdict(clock)


@router.put('/time/set', tags=[Tags.Time])
async def set_clock(user: AuthorisedOperator, s: ClockSetModel) -> str:
    logger.info(f'set_clock - user:{user.uid}')

    clock = Clock.set(s.is_running, s.speed, s.year, s.month, s.day, s.hour, minute=s.minute, second=s.second)
    clock.save(Host)

    return JSONify.as_jdict(clock.now())


@router.patch('/time/run', tags=[Tags.Time])
async def run_clock(user: AuthorisedOperator) -> str:
    logger.info(f'run_clock  - user:{user.uid}')

    clock = Clock.load(Host)
    clock.run()
    clock.save(Host)

    return JSONify.as_jdict(clock.now())


@router.patch('/time/reload', tags=[Tags.Time])
async def reload_clock(user: AuthorisedOperator) -> str:
    logger.info(f'reload_clock  - user:{user.uid}')

    time = PersistentISODatetime.load(Host)
    if time is None:
        raise Conflict409Exception('reload_clock: no saved model time was available')

    clock = Clock.load(Host)
    clock.reload(time)
    clock.save(Host)

    return JSONify.as_jdict(clock.now())


@router.delete('/time/delete', tags=[Tags.Time])
async def delete_conf(user: AuthorisedOperator) -> str:
    logger.info(f'delete_conf  - user:{user.uid}')

    Clock.delete(Host)
    clock = Clock.load(Host)
    return JSONify.as_jdict(clock.now())


# --------------------------------------------------------------------------------------------------------------------

@router.websocket('/time/conf/subscribe')
async def subscribe_conf(socket: WebSocket):
    logger.info(f'subscribe_conf  - socket:{hash(socket)}')
    await ws_manager.connect(socket)

    try:
        while True:
            text = await socket.receive_text()     # needed for heartbeat?
            logger.info(f'subscribe_conf  - text:{text}')

    except WebSocketDisconnect:
        ws_manager.disconnect(socket)
