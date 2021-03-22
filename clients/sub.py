import abc
from .base import BaseRabbitMQClient, AbstractSubscriber

__all__ = [
    'BaseSubscriber'
]


class BaseSubscriber(BaseRabbitMQClient, AbstractSubscriber, abc.ABC):

    """
    Base client for receiving messages from channel
    """

    async def listen(self):
        await self.connect()
        self._logs_exchange = await self.declare_exchange()

        queue = await self.declare_queue()

        # Binding the queue to the exchange
        await queue.bind(self._logs_exchange, routing_key=self.routing_key)

        # Start listening the queue
        await queue.consume(self.on_message)


