import abc
import asyncio
import typing

from aio_pika import (
    Exchange,
    ExchangeType,
    IncomingMessage,
    Message,
    Queue,
    connect_robust,
)
from aio_pika.channel import Channel
from aio_pika.connection import Connection


class AbstractRabbitMQClient(abc.ABC):
    _url: str
    _loop: typing.Optional[asyncio.BaseEventLoop]
    queue_name: str
    exchange_name: str
    exchange_type: ExchangeType
    routing_key: str

    @abc.abstractmethod
    async def connect(self) -> Connection:
        """
        Method that provides connection to broker
        :return: Connection
        """
        pass

    @property
    def url(self) -> str:
        return self._url


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

    @abc.abstractmethod
    async def declare_exchange(self, channel: Channel) -> Exchange:
        """
        Declaring Exchange
        :return: Exchange
        """
        pass

    @abc.abstractmethod
    async def declare_queue(self, channel: Channel) -> Queue:
        """
        Declaring queue
        :return: Queue
        """
        pass


class AbstractPublisher(abc.ABC):

    @abc.abstractmethod
    async def send_message(self, message: Message):
        pass


class BaseRabbitMQClient(AbstractRabbitMQClient):

    def __init__(
            self,
            loop: asyncio.BaseEventLoop = None,
            username='guest',
            password='guest',
            host='localhost'
    ):
        self._loop = loop
        self._url = f'amqp://{username}:{password}@{host}/'

    async def connect(self) -> Connection:
        return await connect_robust(self.url, loop=self._loop)
