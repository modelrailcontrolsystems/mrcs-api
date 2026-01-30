"""
Created on 10 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)

A messaging node that subscribes to, and can publish, clock configurations
"""

from typing import Callable

from mrcs_control.operations.async_messaging_node import AsyncSubscriberNode
from mrcs_control.operations.operation_mode import OperationService
from mrcs_control.operations.time.clock_manager_node import ClockManagerNode

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentFilter, EquipmentType
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import SubscriptionRoutingKey, PublicationRoutingKey
from mrcs_core.operations.time.clock import Clock


# --------------------------------------------------------------------------------------------------------------------

class TimeControllerNode(AsyncSubscriberNode):
    """
    a messaging node that subscribes to, and can publish, clock configurations
    """

    @classmethod
    def id(cls):
        return EquipmentIdentifier(EquipmentType.API, None, 1)


    @classmethod
    def subscription_routing_keys(cls):
        return (SubscriptionRoutingKey(ClockManagerNode.id(), EquipmentFilter.any()), )


    @classmethod
    def publication_routing_key(cls):
        return PublicationRoutingKey(cls.id(), ClockManagerNode.id())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ops: OperationService, client_handler: Callable):
        super().__init__(ops)

        self.__client_handler = client_handler


    # ----------------------------------------------------------------------------------------------------------------

    def handle_message(self, message: Message):
        self.logger.info(f'handle_message: {JSONify.as_jdict(message)}')
        self.client_handler(message)


    # ----------------------------------------------------------------------------------------------------------------

    async def connection_is_available(self):
        await self.mq_client.connection_is_available()


    async def configure_clock(self, clock: Clock):
        self.logger.info(f'configure_clock:{clock}')

        message = Message(self.publication_routing_key(), clock)
        await self.publish(message)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def client_handler(self):
        return self.__client_handler
