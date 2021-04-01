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
        # Perform connection
        connection = await self.connect()

        # Creating a channel
        async with connection.channel() as channel:
            await channel.set_qos(prefetch_count=1)

            # Declare an exchange
            exchange = await self.declare_exchange(channel)

            # Declaring random queue
            queue = await self.declare_queue(channel)

            await queue.bind(exchange, routing_key=self.routing_key)

            # Start listening the random queue
            await queue.consume(self.on_message)
