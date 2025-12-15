"""
Created on 15 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
"""

import json
import os
import unittest

import jwt.help
from fastapi.params import Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient

from mrcs_api.app.main import app
from mrcs_api.models.token import JWT

from mrcs_core.admin.user.user import User
from mrcs_core.data.json import JSONify
from mrcs_core.db.dbclient import DBClient

from mrcs_api.test_setup import TestSetup


# --------------------------------------------------------------------------------------------------------------------

class TestSessionController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TestSetup.dbSetup()


    def setUp(self):
        self.__setup_db()
        self.__client = TestClient(app)


    def tearDown(self):
        DBClient.kill_all()


    def test_log_on(self):
        form = {'grant_type': 'password', 'username': 'bbeloff1@me.com', 'password': 'password'}
        response = self.__client.post('/session/', data=form)
        token = JWT.construct_from_jdict(json.loads(response.content.decode()))
        print(f'token:{token}')


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
