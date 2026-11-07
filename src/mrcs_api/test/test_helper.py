"""
Created on 16 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

Setup and tear down for tests using DB and the app lifespan
"""

from contextlib import AbstractAsyncContextManager

from fastapi import FastAPI

from mrcs_control.db.db_client import DbClient, DbMode


# --------------------------------------------------------------------------------------------------------------------

class TestHelper(object):
    """
    Setup and tear down for tests using DB and the app lifespan
    """


    @classmethod
    def dbSetup(cls):
        if DbClient.client_db_mode() == DbMode.TEST:
            return

        DbClient.kill_all()
        DbClient.set_client_db_mode(DbMode.TEST)


    @classmethod
    def dbTeardown(cls):
        DbClient.kill_all()


    @classmethod
    def sessionSetup(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    # httpx.ASGITransport does not run the app lifespan, so tests must run it themselves. Each
    # IsolatedAsyncioTestCase test has its own event loop, so the lifespan must be entered and exited per test.

    @classmethod
    async def lifespanSetup(cls, app: FastAPI) -> AbstractAsyncContextManager:
        lifespan = app.router.lifespan_context(app)
        await lifespan.__aenter__()

        return lifespan


    @classmethod
    async def lifespanTeardown(cls, lifespan: AbstractAsyncContextManager):
        await lifespan.__aexit__(None, None, None)
