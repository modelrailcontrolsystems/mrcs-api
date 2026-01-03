"""
Created on 13 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
"""

import unittest

from mrcs_api.security.scope import Scope, ScopeDescription

from mrcs_control.db.db_client import DbClient

from mrcs_core.admin.user.user import UserRole


# --------------------------------------------------------------------------------------------------------------------

class TestSession(unittest.TestCase):

    def tearDown(self):
        print('TestTime - tearDown')
        DbClient.kill_all()

    def test_list_scopes(self):
        scopes = list(Scope.keys())
        assert scopes == ['OBSERVE', 'OPERATE_EQUIPMENT', 'ALTER_LAYOUT', 'MANAGE_USER_ACCOUNTS']


    def test_descriptions(self):
        scopes = ScopeDescription.as_dict()
        assert scopes['OBSERVE'] == 'Observe all design and operations.'
        assert scopes['OPERATE_EQUIPMENT'] == 'Operate equipment, observe design.'
        assert scopes['ALTER_LAYOUT'] == 'Operate equipment, alter design.'
        assert scopes['MANAGE_USER_ACCOUNTS'] == 'Operate equipment, alter design and manage user accounts.'


    def test_role_mapping(self):
        scopes = Scope.keys_for_role(UserRole.ADMIN)
        assert scopes == {'OBSERVE', 'OPERATE_EQUIPMENT', 'ALTER_LAYOUT', 'MANAGE_USER_ACCOUNTS'}

        scopes = Scope.keys_for_role(UserRole.DESIGNER)
        assert scopes == {'OBSERVE', 'OPERATE_EQUIPMENT', 'ALTER_LAYOUT'}

        scopes = Scope.keys_for_role(UserRole.OPERATOR)
        assert scopes == {'OBSERVE', 'OPERATE_EQUIPMENT'}

        scopes = Scope.keys_for_role(UserRole.OBSERVER)
        assert scopes == {'OBSERVE', }

