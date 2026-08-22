"""
Created on 6 Dec 2025

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
from mrcs_core.admin.user.user import User
from mrcs_core.data.json import JSONify
from mrcs_core.security.token import JWT


# --------------------------------------------------------------------------------------------------------------------

class TestUserAdmin(unittest.IsolatedAsyncioTestCase):

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

        self.token = await self.__authorise()


    async def asyncTearDown(self):
        await self.__client.aclose()
        DbClient.kill_all()


    async def test_find_all_fail(self):
        response = await self.__client.get('/user/find_all/')
        assert response.status_code == 401


    async def test_find_all(self):
        headers = self.token.as_header()
        response = await self.__client.get('/user/find_all/', headers=headers)

        assert response.status_code == 200
        jdict = response.json()
        assert len(jdict) == 2

        user = User.construct_from_jdict(jdict[0])
        assert user.email == 'bbeloff1@me.com'


    async def test_find_user(self):
        headers = self.token.as_header()
        response = await self.__client.get('/user/find_all/', headers=headers)
        jdict = response.json()
        user = User.construct_from_jdict(jdict[0])

        response = await self.__client.get(f'/user/find/{user.uid}/', headers=headers)
        assert response.status_code == 200

        user = User.construct_from_jdict(response.json())
        assert user.email == 'bbeloff1@me.com'


    async def test_find_self(self):
        headers = self.token.as_header()
        response = await self.__client.get(f'/user/self/', headers=headers)
        assert response.status_code == 200

        user = User.construct_from_jdict(response.json())
        assert user.email == 'bbeloff1@me.com'


    async def test_find_404(self):
        headers = self.token.as_header()
        response = await self.__client.get(f'/user/find/123/', headers=headers)
        assert response.status_code == 404


    async def test_create(self):
        user = self.__load_user('admin_user.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = await self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 201

        created = User.construct_from_jdict(response.json())
        assert created.created is not None

        response = await self.__client.delete(f'/user/delete/{created.uid}/', headers=headers)
        assert response.status_code == 200


    async def test_create_clash(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = await self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 409


    async def test_create_bad_email(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['email'] = 'JUNK'
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = await self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 400


    async def test_create_bad_role(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['role'] = 'JUNK'
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = await self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 400


    async def test_update(self):
        user = self.__load_user('admin_user.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = await self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 201

        created = User.construct_from_jdict(response.json())
        assert created.created is not None

        jdict = JSONify.as_jdict(created)

        response = await self.__client.patch(f'/user/update/', headers=headers, json=jdict)
        assert response.status_code == 200

        response = await self.__client.delete(f'/user/delete/{created.uid}/', headers=headers)
        assert response.status_code == 200


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __load_user(cls, rel_filename):
        abs_filename = Path(__file__).parent / 'data' / rel_filename
        with open(abs_filename) as fp:
            jdict = json.load(fp)

        return User.construct_from_jdict(jdict)


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


    async def __authorise(self) -> JWT:
        form = {'grant_type': 'password', 'username': 'bbeloff1@me.com', 'password': 'pass'}
        response = await self.__client.post('/session', data=form)

        return JWT.construct_from_jdict(json.loads(response.content))
