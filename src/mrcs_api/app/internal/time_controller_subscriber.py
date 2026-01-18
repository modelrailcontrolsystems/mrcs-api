"""
Created on 10 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)

A messaging node that subscribes to, and can publish, clock configurations
"""

from mrcs_control.operations.async_messaging_node import AsyncSubscriberNode
from mrcs_control.operations.operation_mode import OperationService
from mrcs_control.operations.time.clock_manager import ClockManager

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentFilter, EquipmentType
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import SubscriptionRoutingKey, PublicationRoutingKey
from mrcs_core.operations.time.clock import Clock


# --------------------------------------------------------------------------------------------------------------------

class TimeControllerSubscriber(AsyncSubscriberNode):
    """
    a messaging node that subscribes to, and can publish, clock configurations
    """

    @classmethod
    def id(cls):
        return EquipmentIdentifier(EquipmentType.API, None, 1)


    @classmethod
    def subscription_routing_keys(cls):
        return (SubscriptionRoutingKey(ClockManager.id(), EquipmentFilter.all()), )


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ops: OperationService, handler):
        super().__init__(ops)

        self.__handler = handler


    # ----------------------------------------------------------------------------------------------------------------

    def publish_clock(self, clock: Clock):
        self.logger.info(f'publish_clock')

        routing = PublicationRoutingKey(self.id(), ClockManager.id())
        message = Message(routing, clock)

        self.publish(message)


    def handle(self, message: Message):
        self.logger.info(f'handle: {JSONify.as_jdict(message)}')
        self.__handler(message)
