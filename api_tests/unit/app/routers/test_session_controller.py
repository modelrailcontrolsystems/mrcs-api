"""
Created on 15 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
"""

import json
import unittest
from pathlib import Path

import httpx

from mrcs_api.app.main import app
from mrcs_api.test.test_helper import TestHelper
from mrcs_control.admin.user.persistent_user import PersistentUser
from mrcs_control.db.db_client import DbClient
from mrcs_core.security.token import JWT


# --------------------------------------------------------------------------------------------------------------------

class TestSessionController(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        TestHelper.dbSetup()


    @classmethod
    def tearDownClass(cls):
        TestHelper.dbTeardown()


    async def asyncSetUp(self):
        self.__setup_db()
        self.__transport = httpx.ASGITransport(app=app)
        self.__client = httpx.AsyncClient(transport=self.__transport, base_url="http://test", follow_redirects=True)


    async def asyncTearDown(self):
        await self.__client.aclose()
        DbClient.kill_all()


    async def test_log_on(self):
        form = {'grant_type': 'password', 'username': 'bbeloff1@me.com', 'password': 'pass'}
        response = await self.__client.post('/session', data=form)
        assert response.status_code == 201
        token = JWT.construct_from_jdict(json.loads(response.content.decode()))
        assert len(token.access.data) > 100


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __setup_db(cls):
        PersistentUser.recreate_tables()

        abs_filename = Path(__file__).parent / 'data' / 'new_user1.json'
        with open(abs_filename) as fp:
            jdict = json.load(fp)
        obj1 = PersistentUser.construct_from_jdict(jdict)
        obj1 = obj1.save(password='pass')

        abs_filename = Path(__file__).parent / 'data' / 'new_user2.json'
        with open(abs_filename) as fp:
            jdict = json.load(fp)
        obj2 = PersistentUser.construct_from_jdict(jdict)
        obj2 = obj2.save(password='pass')

        DbClient.kill_all()

        return obj1, obj2
