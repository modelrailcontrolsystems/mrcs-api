"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/user/...

User account administration API

http://127.0.0.1:8000/user/find_all
http://127.0.0.1:8000/user/find/def49452-afe0-456a-beac-399c66eb7e95
"""

from typing import List

from fastapi import APIRouter, status

from mrcs_api.app.internal.tags import Tags
from mrcs_api.app.security.authorisation import AuthorisedAdmin, AuthorisedUser
from mrcs_api.exceptions import Conflict409Exception, NotFound404Exception, BadRequest400Exception
from mrcs_api.models.user import APIUser, UserCreateModel, UserUpdateModel, UserModel

from mrcs_control.admin.user.persistent_user import PersistentUser
from mrcs_control.sys.environment import Environment

from mrcs_core.data.json import JSONify
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

env = Environment.get()

Logging.config(env.log_name + ': user_admin', level=env.log_level)
logger = Logging.getLogger()

logger.info('starting')

router = APIRouter(prefix='/user', tags=[Tags.Users])


# --------------------------------------------------------------------------------------------------------------------

@router.get('/find_all')
async def find_all(user: AuthorisedAdmin) -> List[UserModel]:
    logger.info(f'find_all - user:{user.uid}')
    users = list(PersistentUser.find_all())

    return JSONify.as_jdict(users)


@router.get('/find/{uid}')
async def find_user(user: AuthorisedAdmin, uid: str) -> UserModel | None:
    logger.info(f'find_user - user:{user.uid}: uid:{uid}')
    user = PersistentUser.find(uid)

    if not user:
        raise NotFound404Exception(f'find: user {uid} not found')

    return JSONify.as_jdict(user)


@router.get('/self')
async def find_self(user: AuthorisedUser) -> UserModel:
    logger.info(f'find_self - user: {user.uid}')

    return JSONify.as_jdict(user)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(user: AuthorisedAdmin, payload: UserCreateModel) -> UserModel:
    logger.info(f'create - user:{user.uid} payload:{payload}')

    try:
        user = APIUser.construct_from_create_payload(payload)
    except ValueError as ex:
        raise BadRequest400Exception(f'create: {ex}')

    if PersistentUser.email_user(user.email):
        raise Conflict409Exception(f'create: email {user.email} already in use')

    created = user.save(password=payload.password)

    return JSONify.as_jdict(created)


@router.patch('/update')
async def update(user: AuthorisedAdmin, payload: UserUpdateModel) -> None:
    logger.info(f'update - user:{user.uid} payload:{payload}')

    try:
        user = APIUser.construct_from_update_payload(payload)
    except ValueError as ex:
        raise BadRequest400Exception(f'update: {ex}')

    if not PersistentUser.exists(user.uid):
        raise NotFound404Exception(f'update: user {user.uid} not found')

    if PersistentUser.email_user(user.email) != user.uid:
        raise Conflict409Exception(f'update: email {user.email} in use by another user')

    user.save()


@router.delete('/delete/{uid}')
async def delete(user: AuthorisedAdmin, uid: str) -> None:
    logger.info(f'delete - user:{user.uid}: uid:{uid}')

    try:
        PersistentUser.delete(uid)
    except RuntimeError as ex:
        raise Conflict409Exception(f'delete: {ex}')
