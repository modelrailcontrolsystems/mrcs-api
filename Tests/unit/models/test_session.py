"""
Created on 13 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
"""

import unittest

from mrcs_api.models.session import Scope
from mrcs_core.admin.user.user import UserRole


# --------------------------------------------------------------------------------------------------------------------

class TestSession(unittest.TestCase):

    def test_list_scopes(self):
        scopes = list(Scope.keys())
        assert scopes == ['OBSERVE', 'OPERATE', 'LAYOUT', 'USERS']


    def test_descriptions(self):
        scopes = Scope.as_dict()
        assert scopes['OBSERVE'] == 'Observe all design and operations.'
        assert scopes['OPERATE'] == 'Operate equipment, observe design.'
        assert scopes['LAYOUT'] == 'Operate equipment, alter design.'
        assert scopes['USERS'] == 'Administer user accounts.'


    def test_role_mapping(self):
        scopes = Scope.keys_for_role(UserRole.ADMIN)
        assert scopes == {'OBSERVE', 'OPERATE', 'LAYOUT', 'USERS'}

        scopes = Scope.keys_for_role(UserRole.DESIGNER)
        assert scopes == {'OBSERVE', 'OPERATE', 'LAYOUT'}

        scopes = Scope.keys_for_role(UserRole.OPERATOR)
        assert scopes == {'OBSERVE', 'OPERATE'}

        scopes = Scope.keys_for_role(UserRole.OBSERVER)
        assert scopes == {'OBSERVE', }

