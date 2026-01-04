"""
Created on 14 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
"""

import json
import os
import unittest

from datetime import timedelta

from mrcs_api.models.user import APIUser
from mrcs_api.security.token import APIJWT

from mrcs_control.db.db_client import DbClient

from mrcs_core.security.token import TokenData


# --------------------------------------------------------------------------------------------------------------------

class TestToken(unittest.TestCase):

    def tearDown(self):
        print('TestTime - tearDown')
        DbClient.kill_all()

    def test_construct(self):
        user = self.__load_user('saved_user.json')
        delta = timedelta(hours=12)
        jwt = APIJWT.construct(user, delta)

        assert jwt.access.data.sub == user.uid
        assert jwt.access.data.scopes == {'OBSERVE', 'MANAGE_USER_ACCOUNTS', 'OPERATE_EQUIPMENT', 'ALTER_LAYOUT'}
        assert jwt.access.expires_delta == delta


    def test_fail(self):
        user = self.__load_user('new_user.json')
        delta = timedelta(hours=12)

        try:
            APIJWT.construct(user, delta)
        except ValueError as ex:
            assert str(ex) == 'the user must have a valid uid'


    def test_encoded(self):
        user = self.__load_user('saved_user.json')
        delta = timedelta(hours=12)
        jwt = APIJWT.construct(user, delta)
        encoded = jwt.encode()

        assert len(encoded.access_token) > 100
        assert encoded.token_type == 'bearer'


    def test_decoded(self):
        user = self.__load_user('saved_user.json')
        delta = timedelta(hours=12)
        jwt = APIJWT.construct(user, delta)
        encoded = jwt.encode()
        decoded = TokenData.decode(encoded.access_token)

        assert decoded.sub == user.uid
        assert decoded.scopes == {'OBSERVE', 'ALTER_LAYOUT', 'OPERATE_EQUIPMENT', 'MANAGE_USER_ACCOUNTS'}


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __load_user(cls, rel_filename):
        abs_filename = os.path.join(os.path.dirname(__file__), 'data', rel_filename)
        with open(abs_filename) as fp:
            jdict = json.load(fp)

        return APIUser.construct_from_jdict(jdict)


if __name__ == "__main_":
    unittest.main()
