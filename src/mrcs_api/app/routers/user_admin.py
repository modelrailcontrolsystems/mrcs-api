"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

User account administration API

http://127.0.0.1:8000/user/find_all
http://127.0.0.1:8000/user/find/def49452-afe0-456a-beac-399c66eb7e95
"""

from typing import List

from fastapi import APIRouter, HTTPException

from mrcs_api.models.user import APIUser, UserCreateModel, UserUpdateModel, UserModel

from mrcs_core.admin.user.user import User
from mrcs_core.data.json import JSONify
from mrcs_core.sys.environment import Environment
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': user_admin', level=env.log_level)
logger = Logging.getLogger()

logger.info('starting')

router = APIRouter()


# --------------------------------------------------------------------------------------------------------------------

@router.get('/user/find_all', tags=['users'])
async def find_all() -> List[UserModel]:
    logger.info('find_all')
    users = list(User.find_all())

    return JSONify.as_jdict(users)


@router.get('/user/find/{uid}', tags=['users'])
async def find(uid: str) -> UserModel | None:
    logger.info(f'find: {uid}')
    user = User.find(uid)

    if not user:
        raise HTTPException(status_code=404, detail=f'find: user {uid} not found')

    return JSONify.as_jdict(user)


@router.post('/user/create', status_code=201, tags=['users'])
async def create(payload: UserCreateModel) -> UserModel:
    logger.info(f'create: {payload}')

    try:
        user = APIUser.construct_from_create_payload(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=f'create: {ex}')

    if User.email_in_use(user.email):
        raise HTTPException(status_code=409, detail=f'create: email {user.email} already in use')

    created = user.save(password=payload.password)

    return JSONify.as_jdict(created)


@router.put('/user/update', tags=['users'])
async def update(payload: UserUpdateModel) -> None:
    logger.info(f'update: {payload}')

    try:
        user = APIUser.construct_from_update_payload(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=f'update: {ex}')

    if not User.exists(user.uid):
        raise HTTPException(status_code=404, detail=f'update: user {user.uid} not found')

    updated = user.save()

    return JSONify.as_jdict(updated)


@router.delete('/user/delete/{uid}')
async def delete(uid: str) -> None:
    logger.info(f'delete: {uid}')

    try:
        User.delete(uid)
    except RuntimeError as ex:
        raise HTTPException(status_code=409, detail=f'delete: {ex}')

# TODO: log in (put? patch?)
