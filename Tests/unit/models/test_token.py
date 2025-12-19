"""
Created on 14 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
"""

import json
import os
import unittest

from datetime import timedelta

from mrcs_api.models.token import JWT, TokenData
from mrcs_api.models.user import APIUser


# --------------------------------------------------------------------------------------------------------------------

class TestToken(unittest.TestCase):

    def test_construct(self):
        user = self.__load_user('saved_user.json')
        delta = timedelta(hours=12)
        jwt = JWT.construct(user, delta=delta)

        assert jwt.access.data.sub == user.uid
        assert jwt.access.data.scopes == set()
        assert jwt.access.expires_delta == delta


    def test_fail(self):
        user = self.__load_user('new_user.json')
        delta = timedelta(hours=12)

        try:
            JWT.construct(user, delta=delta)
        except ValueError as ex:
            assert str(ex) == 'the user must have a valid uid'


    def test_encoded(self):
        user = self.__load_user('saved_user.json')
        delta = timedelta(hours=12)
        jwt = JWT.construct(user, delta=delta)
        encoded = jwt.encode()

        assert len(encoded.access_token) > 100
        assert encoded.token_type == 'bearer'


    def test_decoded(self):
        user = self.__load_user('saved_user.json')
        delta = timedelta(hours=12)
        jwt = JWT.construct(user, delta=delta)
        encoded = jwt.encode()
        decoded = TokenData.decode(encoded.access_token)

        assert decoded.sub == user.uid
        assert decoded.scopes == set()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __load_user(cls, rel_filename):
        abs_filename = os.path.join(os.path.dirname(__file__), 'data', rel_filename)
        with open(abs_filename) as fp:
            jdict = json.load(fp)

        return APIUser.construct_from_jdict(jdict)


if __name__ == "__main_":
    unittest.main()
