"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

User account administration API

http://127.0.0.1:8000/user/find_all
http://127.0.0.1:8000/user/find/def49452-afe0-456a-beac-399c66eb7e95
"""

from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Security

from mrcs_api.app.routers.session_controller import session_user
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

AuthorizedAdmin = Annotated[User, Security(session_user, scopes=['USERS'])]
AuthorizedUser = Annotated[User, Security(session_user, scopes=[])]


# --------------------------------------------------------------------------------------------------------------------

@router.get('/user/find_all', tags=['users'])
async def find_all(user: AuthorizedAdmin) -> List[UserModel]:
    logger.info(f'find_all - user:{user.uid}')
    users = list(User.find_all())

    return JSONify.as_jdict(users)


@router.get('/user/find/{uid}', tags=['users'])
async def find_user(user: AuthorizedAdmin, uid: str) -> UserModel | None:
    logger.info(f'find_user - user:{user.uid}: uid:{uid}')
    user = User.find(uid)

    if not user:
        raise HTTPException(status_code=404, detail=f'find: user {uid} not found')

    return JSONify.as_jdict(user)


@router.get('/user/self', tags=['users'])
async def find_self(user: AuthorizedUser) -> UserModel | None:
    logger.info(f'find_self - user: {user.uid}')

    return JSONify.as_jdict(user)


@router.post('/user/create', status_code=201, tags=['users'])
async def create(user: AuthorizedAdmin, payload: UserCreateModel) -> UserModel:
    logger.info(f'create - user:{user.uid} payload:{payload}')

    try:
        user = APIUser.construct_from_create_payload(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=f'create: {ex}')

    if User.email_in_use(user.email):
        raise HTTPException(status_code=409, detail=f'create: email {user.email} already in use')

    created = user.save(password=payload.password)

    return JSONify.as_jdict(created)


@router.put('/user/update', tags=['users'])
async def update(user: AuthorizedAdmin, payload: UserUpdateModel) -> None:
    logger.info(f'update - user:{user.uid} payload:{payload}')

    try:
        user = APIUser.construct_from_update_payload(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=f'update: {ex}')

    if not User.exists(user.uid):
        raise HTTPException(status_code=404, detail=f'update: user {user.uid} not found')

    user.save()


@router.delete('/user/delete/{uid}', tags=['users'])
async def delete(user: AuthorizedAdmin, uid: str) -> None:
    logger.info(f'delete - user:{user.uid}: uid:{uid}')

    try:
        User.delete(uid)
    except RuntimeError as ex:
        raise HTTPException(status_code=409, detail=f'delete: {ex}')
