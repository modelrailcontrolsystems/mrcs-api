"""
Created on 19 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a JavaScript Web Token (JWT) - received via the API
"""

from pydantic import BaseModel


# --------------------------------------------------------------------------------------------------------------------

class TokenModel(BaseModel):
    access_token: str
    token_type: str
