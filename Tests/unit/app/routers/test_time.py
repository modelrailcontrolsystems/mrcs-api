"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
"""

import json
import unittest

from fastapi.testclient import TestClient

from mrcs_api.app.main import app

from mrcs_control.db.dbclient import DBClient

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.operations.time.clock import Clock
from mrcs_core.security.token import JWT


# --------------------------------------------------------------------------------------------------------------------

class TestTime(unittest.TestCase):

    token: JWT = None

    def setUp(self):
        self.__client = TestClient(app)

        if self.token is None:
            self.token = self.__authorise()

    def tearDown(self):
        DBClient.kill_all()


    def test_now(self):
        response = self.__client.get('/time/now/')
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None

    def test_conf(self):
        response = self.__client.get('/time/conf/')
        assert response.status_code == 200
        conf = Clock.construct_from_jdict(response.json())
        assert conf is not None

    def test_set(self):
        headers = self.token.as_header()
        conf = {'is_running': True, 'speed': 4, 'year': 2025, 'month': 1, 'day': 2, 'hour': 6}
        response = self.__client.put('/time/set/', headers=headers, json=conf)
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None

    def test_start(self):
        headers = self.token.as_header()
        response = self.__client.patch('/time/start/', headers=headers)
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None

    def test_delete(self):
        headers = self.token.as_header()
        response = self.__client.delete('/time/delete/', headers=headers)
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None


    # ----------------------------------------------------------------------------------------------------------------

    def __authorise(self) -> JWT:
        form = {'grant_type': 'password', 'username': 'bbeloff1@me.com', 'password': 'pass'}
        response = self.__client.post('/session/', data=form)

        return JWT.construct_from_jdict(json.loads(response.content))
