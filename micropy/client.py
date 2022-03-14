import inspect
import json
from typing import Callable, Optional, List

from micropy.brokers.base import MicropyRpcProducerBase, encode as micropy_encode, decode as micropy_decode
from micropy.brokers.default import DefaultRpcProducer
from micropy.exceptions import MicropyUnRecognizeExceptions


class _RpcClient:

    def __init__(self, queue_name):
        self._broker: MicropyRpcProducerBase = DefaultRpcProducer(queue_name)

    def rpc_call(self, method_name: str, raise_exceptions: Optional[List], *args, **kwargs) -> any:
        message = {'func': method_name, 'args': args, 'kwargs': kwargs}
        response = self._broker.rcp_call(micropy_encode(json.dumps(message)))
        response_message = json.loads(micropy_decode(response))
        return _RpcClient._handle_rpc_response(response_message, raise_exceptions)

    @staticmethod
    def _handle_rpc_response(response_message: dict, raise_exceptions: Optional[List]) -> any:
        raise_class = response_message.get('raise_class', None)
        if not raise_class:
            return response_message['return_value']

        builtin_exception = globals()['__builtins__'].get(raise_class[0], None)
        if builtin_exception:
            raise builtin_exception(raise_class[1])

        name_to_exception_map = {exception.__class__.__name__: exception for exception in raise_exceptions or []}
        if raise_class[0] in name_to_exception_map.keys():
            raise name_to_exception_map[raise_class[0]][raise_class[1]]

        raise MicropyUnRecognizeExceptions(raise_class[1])


def micropy_rpc_client(queue_name: str) -> Callable:
    def inner(cls):
        def wrap(_method: Callable):
            def method_wrapper(self, *args, **kwargs):
                self.__client = self.__dict__.get('__client', None) or _RpcClient(queue_name)
                raise_exceptions = _method.__dict__.get('micropy_raise_exceptions', None)
                return self.__client.rpc_call(_method.__name__, raise_exceptions, *args, **kwargs)
            return method_wrapper

        # TODO: skip static method and class method
        for method_name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if method_name.startswith('_'):
                continue
            setattr(cls, method_name, wrap(method))
        return cls
    return inner


def micropy_rpc_catch(exceptions: List) -> Callable:
    def inner(func):
        func.micropy_raise_exceptions = exceptions
        return func
    return inner
