"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
"""

import json
import os
import unittest

from fastapi.testclient import TestClient

from mrcs_api.app.main import app
from mrcs_api.test_setup import TestSetup

from mrcs_control.admin.user.user import PersistentUser
from mrcs_control.db.dbclient import DBClient

from mrcs_core.admin.user.user import User
from mrcs_core.data.json import JSONify
from mrcs_core.security.token import JWT


# --------------------------------------------------------------------------------------------------------------------

class TestUserAdmin(unittest.TestCase):

    token: JWT = None

    @classmethod
    def setUpClass(cls):
        TestSetup.dbSetup()


    def setUp(self):
        self.__setup_db()
        self.__client = TestClient(app)

        if self.token is None:
            self.token = self.__authorise()


    def tearDown(self):
        DBClient.kill_all()


    def test_find_all_fail(self):
        response = self.__client.get('/user/find_all/')
        assert response.status_code == 401


    def test_find_all(self):
        headers = self.token.as_header()
        response = self.__client.get('/user/find_all/', headers=headers)

        assert response.status_code == 200
        jdict = response.json()
        assert len(jdict) == 2

        user = User.construct_from_jdict(jdict[0])
        assert user.email == 'bbeloff1@me.com'


    def test_find_user(self):
        headers = self.token.as_header()
        response = self.__client.get('/user/find_all/', headers=headers)
        jdict = response.json()
        user = User.construct_from_jdict(jdict[0])

        response = self.__client.get(f'/user/find/{user.uid}/', headers=headers)
        assert response.status_code == 200

        user = User.construct_from_jdict(response.json())
        assert user.email == 'bbeloff1@me.com'


    def test_find_self(self):
        headers = self.token.as_header()
        response = self.__client.get(f'/user/self/', headers=headers)
        assert response.status_code == 200

        user = User.construct_from_jdict(response.json())
        print(f'user:{user}')
        assert user.email == 'bbeloff1@me.com'


    def test_find_404(self):
        headers = self.token.as_header()
        response = self.__client.get(f'/user/find/123/', headers=headers)
        assert response.status_code == 404


    def test_create(self):
        user = self.__load_user('admin_user.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 201

        created = User.construct_from_jdict(response.json())
        assert created.created is not None

        response = self.__client.delete(f'/user/delete/{created.uid}/', headers=headers)
        assert response.status_code == 200


    def test_create_clash(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 409


    def test_create_bad_email(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['email'] = 'JUNK'
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 400


    def test_create_bad_role(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['role'] = 'JUNK'
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 400


    def test_update(self):
        user = self.__load_user('admin_user.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        headers = self.token.as_header()
        response = self.__client.post('/user/create/', headers=headers, json=jdict)
        assert response.status_code == 201

        created = User.construct_from_jdict(response.json())
        assert created.created is not None

        jdict = JSONify.as_jdict(created)

        response = self.__client.put(f'/user/update/', headers=headers, json=jdict)
        assert response.status_code == 200

        response = self.__client.delete(f'/user/delete/{created.uid}/', headers=headers)
        assert response.status_code == 200


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __load_user(cls, rel_filename):
        abs_filename = os.path.join(os.path.dirname(__file__), 'data', rel_filename)
        with open(abs_filename) as fp:
            jdict = json.load(fp)

        return User.construct_from_jdict(jdict)


    @classmethod
    def __setup_db(cls):
        PersistentUser.recreate_tables()

        abs_filename = os.path.join(os.path.dirname(__file__), 'data', 'new_user1.json')
        with open(abs_filename) as fp:
            jdict = json.load(fp)
        obj1 = PersistentUser.construct_from_jdict(jdict)
        obj1 = obj1.save(password='pass')

        abs_filename = os.path.join(os.path.dirname(__file__), 'data', 'new_user2.json')
        with open(abs_filename) as fp:
            jdict = json.load(fp)
        obj2 = PersistentUser.construct_from_jdict(jdict)
        obj2 = obj2.save(password='pass')

        DBClient.kill_all()

        return obj1, obj2


    def __authorise(self) -> JWT:
        form = {'grant_type': 'password', 'username': 'bbeloff1@me.com', 'password': 'pass'}
        response = self.__client.post('/session/', data=form)

        return JWT.construct_from_jdict(json.loads(response.content))
