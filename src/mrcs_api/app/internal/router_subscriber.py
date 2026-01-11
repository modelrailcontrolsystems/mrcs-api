"""
Created on 10 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)

A universal message logger
"""

from mrcs_control.operations.messaging_node import SubscriberNode
from mrcs_control.operations.operation_mode import OperationService

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentFilter, EquipmentType
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import SubscriptionRoutingKey


# --------------------------------------------------------------------------------------------------------------------

class RouterSubscriber(SubscriberNode):
    """
    A universal message logger
    """

    @classmethod
    def identity(cls):
        return EquipmentIdentifier(EquipmentType.IAP, None, 1)


    @classmethod
    def routing_keys(cls):
        return (SubscriptionRoutingKey(EquipmentFilter.all(), EquipmentFilter.all()), )


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ops: OperationService, handler):
        super().__init__(ops)

        self.__handler = handler
        self.__is_subscribing = False


    # ----------------------------------------------------------------------------------------------------------------

    def subscribe(self):
        self.logger.info(f'*** subscribe - identity:{self.identity()}, is_subscribing:{self.is_subscribing}')
        if self.is_subscribing:
            return

        self.mq_client.connect()

        try:
            self.mq_client.subscribe(*self.routing_keys())
        except KeyboardInterrupt:
            return


    # ----------------------------------------------------------------------------------------------------------------

    def handle(self, message: Message):
        self.logger.info(f'handle: {message}')
        self.__handler(message)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_subscribing(self):
        return self.__is_subscribing


    @is_subscribing.setter
    def is_subscribing(self, is_subscribing):
        self.__is_subscribing = is_subscribing


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        routing_keys = [str(key) for key in self.routing_keys()]
        return (f'{self.__class__.__name__}:{{identity:{self.identity()}, is_subscribing:{self.is_subscribing}, '
                f'routing_keys:{routing_keys}, ops:{self.ops}, mq_client:{self.mq_client}}}')
