"""
Created on 14 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

A JSON Web Token (JWT) carrying scopes

https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#verify-the-scopes
"""

import jwt

from collections import OrderedDict
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel

from mrcs_api.models.session import Scope

from mrcs_core.admin.user.user import User
from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class TokenModel(BaseModel):
    access_token: str
    token_type: str


# --------------------------------------------------------------------------------------------------------------------

class TokenData(JSONable):
    """
    The data component of an AccessToken, carrying scopes
    """

    SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    ALGORITHM = 'HS256'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def decode(cls, token: str):
        payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        username = payload.get('sub')

        if username is None:
            raise ValueError('the username may not be None')

        scope: str = payload.get('scope', '')
        scopes = set(scope.split(' '))

        return cls(username, scopes)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sub: str, scopes: set):
        self.__sub = sub
        self.__scopes = scopes


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, expiry=None):
        jdict = OrderedDict()

        jdict['sub'] = self.sub
        jdict['scope'] = ' '.join(self.scopes)

        if expiry:
            jdict['exp'] = expiry

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sub(self):
        return self.__sub


    @property
    def scopes(self):
        return self.__scopes


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'TokenData:{{sub:{self.sub}, scopes:{self.scopes}}}'


# --------------------------------------------------------------------------------------------------------------------

class AccessToken(object):
    """
    The access component of a JWT
    """

    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, data: TokenData, expires_delta: timedelta | None):
        self.__data = data
        self.__expires_delta = expires_delta


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def data(self):
        return self.__data


    @property
    def expires_delta(self):
        return self.__expires_delta


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'AccessToken:{{data:{self.data}, expires_delta:{self.expires_delta}}}'


# --------------------------------------------------------------------------------------------------------------------

class JWT(object):
    """
    A JSON Web Token (JWT), carrying scopes
    """

    TOKEN_TYPE = 'bearer'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        token_type = jdict.get('token_type')
        access = AccessToken(jdict.get('access_token'), None)

        return cls(access, token_type)


    @classmethod
    def construct(cls, user: User, delta: timedelta | None = None):
        if not user.uid:
            raise ValueError('the user must have a valid uid')

        scopes = Scope.keys_for_role(user.role)
        expires_delta = timedelta(minutes=AccessToken.ACCESS_TOKEN_EXPIRE_MINUTES) if delta is None else delta

        data = TokenData(user.uid, scopes)
        access = AccessToken(data, expires_delta)

        return cls(access)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, access: AccessToken, token_type: str = TOKEN_TYPE):
        self.__access = access
        self.__token_type = token_type


    # ----------------------------------------------------------------------------------------------------------------

    def encode(self):
        expiry = datetime.now(timezone.utc) + self.access.expires_delta
        data = self.access.data.as_json(expiry=expiry)

        encoded_jwt = jwt.encode(data, TokenData.SECRET_KEY, algorithm=TokenData.ALGORITHM)

        return TokenModel(access_token=encoded_jwt, token_type=self.token_type)


    def as_header(self):
        return {'Authorization': f'{self.token_type.capitalize()} {self.access.data}'}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def access(self):
        return self.__access


    @property
    def token_type(self):
        return self.__token_type


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'JWT:{{access:{self.access}, token_type:{self.token_type}}}'
