import abc
from .base import BaseRabbitMQClient, AbstractPublisher


__all__ = [
    'BasePublisher'
]


class BasePublisher(BaseRabbitMQClient,
                    AbstractPublisher,
                    abc.ABC):
    """
    Base client for publishing messages to channel
    """
