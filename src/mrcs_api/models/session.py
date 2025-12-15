"""
Created on 13 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the possible security scopes

https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#verify-the-scopes
"""

from enum import Enum

from mrcs_core.admin.user.user import UserRole
from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

class Scope(Enum, metaclass=MetaEnum):
    """
    An enumeration of all the possible security scopes
    """

    OBSERVE =   'Observe all design and operations.'
    OPERATE =   'Operate equipment, observe design.'
    LAYOUT =    'Operate equipment, alter design.'
    USERS =     'Administer user accounts.'

    @classmethod
    def as_dict(cls):
        return {key: cls[key].value for key in cls.keys()}


    # ----------------------------------------------------------------------------------------------------------------

    __ROLE_MAPPING = {
        UserRole.ADMIN:     {'OBSERVE', 'OPERATE', 'LAYOUT', 'USERS'},
        UserRole.DESIGNER:  {'OBSERVE', 'OPERATE', 'LAYOUT'},
        UserRole.OPERATOR:  {'OBSERVE', 'OPERATE'},
        UserRole.OBSERVER:  {'OBSERVE', },
    }

    @classmethod
    def keys_for_role(cls, role: UserRole):
        try:
            return cls.__ROLE_MAPPING[role]
        except KeyError:
            return []
