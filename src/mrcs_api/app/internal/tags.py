#!/usr/bin/env python3

"""
Created on 18 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/docs

https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
"""

from enum import StrEnum


# --------------------------------------------------------------------------------------------------------------------

class Tags(StrEnum):
    Messages = 'Messages'
    Session = 'Session'
    Time = 'Time'
    Users = 'Users'
