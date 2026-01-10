"""
Created on 9 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)

https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients
"""

from fastapi import WebSocket


# --------------------------------------------------------------------------------------------------------------------

class WebSocketManager(object):
    """
    stuff
    """

    def __init__(self, logger):
        self.__sockets: dict[int, WebSocket] = {}
        self.__logger = logger


    # ----------------------------------------------------------------------------------------------------------------

    async def connect(self, socket: WebSocket):
        await socket.accept()
        self.__sockets[hash(socket)] = socket
        self.__logger.info(f'connect:{self}')


    def disconnect(self, socket):
        self.__sockets.pop(hash(socket), None)
        self.__logger.info(f'disconnect:{self}')


    async def broadcast(self, jdict: dict):
        self.__logger.info(f'broadcast:{self}')

        for id, socket in list(self.__sockets.items()):
            try:
                await socket.send_json(jdict)
            except RuntimeError:
                self.__sockets.pop(id, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'WebSocketManager:{{sockets:{list(self.__sockets.keys())}}}'
