"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
"""

import json
import unittest

import httpx

from mrcs_api.app.main import app
from mrcs_api.test.test_helper import TestHelper
from mrcs_control.db.db_client import DbClient
from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.operations.time.clock import Clock
from mrcs_core.security.token import JWT
from mrcs_core.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class TestTime(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        TestHelper.dbSetup()


    @classmethod
    def tearDownClass(cls):
        Clock.delete(Host)
        TestHelper.dbTeardown()


    async def asyncSetUp(self):
        self.__transport = httpx.ASGITransport(app=app)
        self.__client = httpx.AsyncClient(transport=self.__transport, base_url="http://test", follow_redirects=True)

        self.token = await self.__authorise()


    async def asyncTearDown(self):
        await self.__client.aclose()
        DbClient.kill_all()


    async def test_now(self):
        response = await self.__client.get('/time/now/')
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None


    async def test_conf(self):
        response = await self.__client.get('/time/conf/')
        assert response.status_code == 200
        conf = Clock.construct_from_jdict(response.json())
        assert conf is not None


    async def test_set(self):
        headers = self.token.as_header()
        conf = {'is_running': True, 'speed': 4, 'year': 2025, 'month': 1, 'day': 2, 'hour': 6}
        response = await self.__client.put('/time/set/', headers=headers, json=conf)
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None


    async def test_run(self):
        clock = Clock.set(False, 4, 2025, 1, 2, 6)
        clock.save(Host)

        headers = self.token.as_header()
        response = await self.__client.patch('/time/run/', headers=headers)
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None


    async def test_delete(self):
        headers = self.token.as_header()
        response = await self.__client.delete('/time/delete/', headers=headers)
        assert response.status_code == 200
        now = ISODatetime.construct_from_jdict(response.json())
        assert now is not None


    # ----------------------------------------------------------------------------------------------------------------

    async def __authorise(self) -> JWT:
        form = {'grant_type': 'password', 'username': 'bbeloff1@me.com', 'password': 'pass'}
        response = await self.__client.post('/session', data=form)

        return JWT.construct_from_jdict(json.loads(response.content))
