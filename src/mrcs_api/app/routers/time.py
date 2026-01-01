"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/time

Time API
"""

from fastapi import APIRouter

from mrcs_api.app.internal.tags import Tags
from mrcs_api.app.security.authorisation import AuthorisedOperator
from mrcs_api.models.time import ClockSetModel, ClockConfModel

from mrcs_control.sys.environment import Environment

from mrcs_core.data.json import JSONify
from mrcs_core.operations.time.clock import Clock
from mrcs_core.sys.host import Host

from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': time', level=env.log_level)
logger = Logging.getLogger()

logger.info(f'starting')

router = APIRouter()


# --------------------------------------------------------------------------------------------------------------------

@router.get('/time/now', tags=[Tags.Time])
async def now() -> str:
    logger.info(f'now')

    clock = Clock.load(Host, skeleton=True)
    return JSONify.as_jdict(clock.now())


@router.get('/time/conf', tags=[Tags.Time])
async def conf() -> ClockConfModel:
    logger.info(f'conf')

    clock = Clock.load(Host, skeleton=True)
    return JSONify.as_jdict(clock)


@router.put('/time/set', tags=[Tags.Time])
async def set_clock(user: AuthorisedOperator, s: ClockSetModel) -> str:
    logger.info(f'set_clock - user:{user.uid}')

    clock = Clock.set(s.is_running, s.speed, s.year, s.month, s.day, s.hour, minute=s.minute, second=s.second)
    clock.save(Host)

    return JSONify.as_jdict(clock.now())


@router.patch('/time/start', tags=[Tags.Time])
async def start_clock(user: AuthorisedOperator) -> str:
    logger.info(f'start_clock  - user:{user.uid}')

    clock = Clock.load(Host, skeleton=True)
    clock.start()
    clock.save(Host)

    return JSONify.as_jdict(clock.now())


@router.delete('/time/delete', tags=[Tags.Time])
async def delete_conf(user: AuthorisedOperator) -> str:
    logger.info(f'delete_conf  - user:{user.uid}')

    Clock.delete(Host)
    clock = Clock.load(Host, skeleton=True)
    return JSONify.as_jdict(clock.now())
