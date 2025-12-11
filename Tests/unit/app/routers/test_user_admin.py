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

from mrcs_core.admin.user.user import User
from mrcs_core.data.json import JSONify
from mrcs_core.db.dbclient import DBClient

from setup import Setup


# --------------------------------------------------------------------------------------------------------------------

class TestUserAdmin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Setup()


    def setUp(self):
        self.__setup_db()
        self.__client = TestClient(app)


    def tearDown(self):
        DBClient.kill_all()


    def test_find_all(self):
        response = self.__client.get('/user/find_all/')
        assert response.status_code == 200
        jdict = response.json()
        assert len(jdict) == 2

        user = User.construct_from_jdict(jdict[0])
        assert user.email == 'bbeloff1@me.com'


    def test_find(self):
        response = self.__client.get('/user/find_all/')
        jdict = response.json()
        user = User.construct_from_jdict(jdict[0])

        response = self.__client.get(f'/user/find/{user.uid}/')
        assert response.status_code == 200

        user = User.construct_from_jdict(response.json())
        assert user.email == 'bbeloff1@me.com'


    def test_find_404(self):
        response = self.__client.get(f'/user/find/123/')
        assert response.status_code == 404


    def test_create(self):
        user = self.__load_user('admin_user.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        response = self.__client.post('/user/create/', json=jdict)
        assert response.status_code == 201

        created = User.construct_from_jdict(response.json())
        assert created.created is not None

        response = self.__client.delete(f'/user/delete/{created.uid}/')
        assert response.status_code == 200


    def test_create_clash(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        response = self.__client.post('/user/create/', json=jdict)
        assert response.status_code == 409


    def test_create_bad_email(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['email'] = 'JUNK'
        jdict['password'] = 'pass'
        response = self.__client.post('/user/create/', json=jdict)
        assert response.status_code == 400


    def test_create_bad_role(self):
        user = self.__load_user('new_user1.json')
        jdict = JSONify.as_jdict(user)
        jdict['role'] = 'JUNK'
        jdict['password'] = 'pass'
        response = self.__client.post('/user/create/', json=jdict)
        assert response.status_code == 400


    def test_update(self):
        user = self.__load_user('admin_user.json')
        jdict = JSONify.as_jdict(user)
        jdict['password'] = 'pass'
        response = self.__client.post('/user/create/', json=jdict)
        assert response.status_code == 201

        created = User.construct_from_jdict(response.json())
        assert created.created is not None

        jdict = JSONify.as_jdict(created)

        response = self.__client.put(f'/user/update/', json=jdict)
        assert response.status_code == 200

        response = self.__client.delete(f'/user/delete/{created.uid}/')
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
        User.recreate_tables()

        abs_filename = os.path.join(os.path.dirname(__file__), 'data', 'new_user1.json')
        with open(abs_filename) as fp:
            jdict = json.load(fp)
        obj1 = User.construct_from_jdict(jdict)
        obj1 = obj1.save(password='password')

        abs_filename = os.path.join(os.path.dirname(__file__), 'data', 'new_user2.json')
        with open(abs_filename) as fp:
            jdict = json.load(fp)
        obj2 = User.construct_from_jdict(jdict)
        obj2 = obj2.save(password='password')

        DBClient.kill_all()

        return obj1, obj2
