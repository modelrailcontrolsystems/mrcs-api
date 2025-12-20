"""
Created on 15 Dec 2025

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

from mrcs_core.security.token import JWT


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
        form = {'grant_type': 'password', 'username': 'bbeloff1@me.com', 'password': 'pass'}
        response = self.__client.post('/session/', data=form)
        assert response.status_code == 201
        token = JWT.construct_from_jdict(json.loads(response.content.decode()))
        assert len(token.access.data) > 100


    # ----------------------------------------------------------------------------------------------------------------

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
