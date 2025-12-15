"""
Created on 16 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

Set up tests to use the test DB
"""

from mrcs_core.db.dbclient import DBClient, DBMode


# --------------------------------------------------------------------------------------------------------------------

class TestSetup(object):
    """
    Set up tests to use the test DB
    """

    @classmethod
    def dbSetup(cls):
        print('*** mrcs_api: dbSetup')

        if DBClient.client_db_mode() == DBMode.TEST:
            return

        DBClient.kill_all()
        DBClient.set_client_db_mode(DBMode.TEST)


    @classmethod
    def sessionSetup(cls):
        # grant_type=password&username=bbeloff1%40me.com&password=password
        print('*** mrcs_api: sessionSetup')
        pass

