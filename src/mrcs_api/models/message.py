"""
Created on 3 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message - received via the API
"""

from typing import Dict

from pydantic import BaseModel

from mrcs_core.messaging.message import Message


# --------------------------------------------------------------------------------------------------------------------

class MessageModel(BaseModel):
    routing: str
    body: Dict


class MessageRecordModel(BaseModel):
    uid: int
    rec: str
    routing: str
    body: Dict


# --------------------------------------------------------------------------------------------------------------------

class APIMessage(Message):
    """A structured representation of a message"""

    @classmethod
    def construct_from_payload(cls, payload: MessageModel):
        return cls.construct_from_jdict(payload.model_dump())

