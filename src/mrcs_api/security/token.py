"""
Created on 19 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

A JSON Web Token (JWT) carrying scopes

https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#verify-the-scopes
"""

from datetime import datetime, timedelta, timezone

import jwt

from mrcs_api.models.user import APIUser
from mrcs_core.security.token import AccessToken, JWT, TokenData


# --------------------------------------------------------------------------------------------------------------------

class APIJWT(JWT):
    """
    A JSON Web Token (JWT), carrying scopes
    """


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, user: APIUser, expires_delta: timedelta):
        if not user.uid:
            raise ValueError('the user must have a valid uid')

        data = TokenData(user.uid, user.scopes())
        access = AccessToken(data, expires_delta)

        return cls(access)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, access: AccessToken, token_type: str = JWT.TOKEN_TYPE):
        super().__init__(access, token_type)


    # ----------------------------------------------------------------------------------------------------------------

    def encode(self):
        expiry = datetime.now(timezone.utc) + self.access.expires_delta
        data = self.access.data.as_json(expiry=expiry)
        encoded_jwt = jwt.encode(data, TokenData.SECRET_KEY, algorithm=TokenData.ALGORITHM)

        return TokenModel(access_token=encoded_jwt, token_type=self.token_type)
