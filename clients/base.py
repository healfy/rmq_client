import abc
import asyncio
from aio_pika import (
    connect,
    Exchange,
    ExchangeType,
    IncomingMessage,
    Queue,
    Message
)
from aio_pika.connection import Connection
from aio_pika.channel import Channel


class AbstractRabbitMQClient(abc.ABC):
    _url: str
    _loop: asyncio.BaseEventLoop
    _connection: Connection
    _channel: Channel
    _logs_exchange: Exchange
    queue_name: str 
    exchange_name: str
    exchange_type: ExchangeType
    routing_key: str
    
    @abc.abstractmethod
    async def connect(self):
        """
        Method that provides connection to broker
        :return: None 
        """
        pass
    
    @property
    def url(self) -> str:
        return self._url

    @abc.abstractmethod
    async def declare_exchange(self) -> Exchange:
        """
        Declaring Exchange
        :return: Exchange
        """
        pass

    @abc.abstractmethod
    async def declare_queue(self) -> Queue:
        """
        Declaring queue
        :return: Queue
        """
        pass


class AbstractSubscriber(abc.ABC):

    @abc.abstractmethod
    async def listen(self):
        """
        Method to start receiving messages from channel
        :return: None
        """
        pass

    @abc.abstractmethod
    async def on_message(self, message: IncomingMessage):
        """
        Handler that holds business logic
        :param message: IncomingMessage
        :return: None
        """
        pass


class AbstractPublisher(abc.ABC):

    @abc.abstractmethod
    async def send_message(self, message: Message):
        pass


class BaseRabbitMQClient(AbstractRabbitMQClient):
        
    def __init__(
            self, 
            loop: asyncio.BaseEventLoop,
            username='guest',
            password='guest',
            host='localhost'
    ):
        self._loop = loop
        self._url = f'amqp://{username}:{password}@{host}/'
    
    async def connect(self):
        self._connection = await connect(self.url, loop=self._loop)
        self._channel = self._connection.channel()
        await self._channel.set_qos(prefetch_count=1)
    
    async def declare_exchange(self) -> Exchange:
        return await self._channel.declare_exchange(
            self.exchange_name, self.exchange_type
        )
    
    async def declare_queue(self) -> Queue:

        return await self._channel.declare_queue(
            f'{self.queue_name}_queue', exclusive=True, durable=True
        )
