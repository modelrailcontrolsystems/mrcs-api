#!/usr/bin/env python3

"""
Created on 18 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

http://127.0.0.1:8000/
http://127.0.0.1:8000/docs

https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
"""

from enum import StrEnum, Enum

from mrcs_core.admin.user.user import UserRole
from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

class ScopeDescription(Enum, metaclass=MetaEnum):
    """
    An enumeration of all the possible security scopes
    """

    OBSERVE =               'Observe all design and operations.'
    OPERATE_EQUIPMENT =     'Operate equipment, observe design.'
    ALTER_LAYOUT =          'Operate equipment, alter design.'
    MANAGE_USER_ACCOUNTS =  'Operate equipment, alter design and manage user accounts.'

    @classmethod
    def as_dict(cls):
        return {key: cls[key].value for key in cls.keys()}


# --------------------------------------------------------------------------------------------------------------------

class Scope(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible security scopes
    """

    OBSERVE =               'OBSERVE'
    OPERATE_EQUIPMENT =     'OPERATE_EQUIPMENT'
    ALTER_LAYOUT =          'ALTER_LAYOUT'
    MANAGE_USER_ACCOUNTS =  'MANAGE_USER_ACCOUNTS'

    # ----------------------------------------------------------------------------------------------------------------

    __ROLE_MAPPING = {
        UserRole.ADMIN:     {OBSERVE, OPERATE_EQUIPMENT, ALTER_LAYOUT, MANAGE_USER_ACCOUNTS},
        UserRole.DESIGNER:  {OBSERVE, OPERATE_EQUIPMENT, ALTER_LAYOUT},
        UserRole.OPERATOR:  {OBSERVE, OPERATE_EQUIPMENT},
        UserRole.OBSERVER:  {OBSERVE, },
    }

    @classmethod
    def keys_for_role(cls, role: UserRole):
        try:
            return cls.__ROLE_MAPPING[role]
        except KeyError:
            return []
