import abc

from aio_pika import Channel, Exchange, Queue

from .base import AbstractSubscriber, BaseRabbitMQClient

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
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        # Declare an exchange
        exchange = await self.declare_exchange(channel)

        # Declaring random queue
        queue = await self.declare_queue(channel)

        await queue.bind(exchange, routing_key=self.routing_key)

        # Start listening the random queue
        await queue.consume(self.on_message)

    async def declare_exchange(self, channel: Channel) -> Exchange:
        return await channel.declare_exchange(
            self.exchange_name, self.exchange_type
        )

    async def declare_queue(self, channel: Channel) -> Queue:
        return await channel.declare_queue(
            f'{self.queue_name}_queue', durable=True
        )
