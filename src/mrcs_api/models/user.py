"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a user - received via the API
"""

from pydantic import BaseModel, ConfigDict

from mrcs_api.app.security.scope import Scope
from mrcs_control.admin.user.user import PersistentUser

from mrcs_core.admin.user.user import UserRole
from mrcs_core.data.iso_datetime import ISODatetime


# ----------------------------------------------------------------------------------------------------------------

class UserModel(BaseModel):
    model_config = ConfigDict(extra='allow')

    uid: str
    email: str
    role: str
    must_set_password: bool
    given_name: str
    family_name: str
    created: str
    latest_login: str | None


class UserCreateModel(BaseModel):
    model_config = ConfigDict(extra='allow')

    email: str
    password: str
    role: str
    must_set_password: bool
    given_name: str
    family_name: str


class UserUpdateModel(BaseModel):
    model_config = ConfigDict(extra='allow')

    uid: str
    email: str
    role: str
    given_name: str
    family_name: str


# --------------------------------------------------------------------------------------------------------------------

class APIUser(PersistentUser):

    @classmethod
    def construct_from_create_payload(cls, payload: UserCreateModel):
        return cls.construct_from_jdict(payload.model_dump())


    @classmethod
    def construct_from_update_payload(cls, payload: UserUpdateModel):
        return cls.construct_from_jdict(payload.model_dump())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uid: str | None, email: str, role: UserRole, must_set_password: bool,
                 given_name: str, family_name: str, created: ISODatetime | None, latest_login: ISODatetime | None):
        super().__init__(uid, email, role, must_set_password, given_name, family_name, created, latest_login)


    # ----------------------------------------------------------------------------------------------------------------

    def scopes(self):
        return Scope.keys_for_role(self.role)
