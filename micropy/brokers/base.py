from abc import abstractmethod, ABC
from typing import Callable


class MicropyRpcProducerBase(ABC):

    def __init__(self, queue_name: str):
        self._queue_name = queue_name

    @abstractmethod
    def rcp_call(self, message: bytes) -> bytes:
        pass


class MicropyRpcConsumerBase(ABC):
    def __init__(self, queue_name: str):
        self._queue_name = queue_name

    @abstractmethod
    def listen(self, on_request: Callable) -> None:
        pass


def encode(message: str) -> bytes:
    return message.encode('utf-8')


def decode(message: bytes) -> str:
    return message.decode('utf-8')
