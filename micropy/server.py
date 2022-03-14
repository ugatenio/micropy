import json
import traceback

from micropy.brokers.base import MicropyRpcConsumerBase, encode as micropy_encode
from micropy.brokers.default import DefaultRpcConsumer


class MicropyRpcProducer:

    def __init__(self, queue_name: str):
        self._broker: MicropyRpcConsumerBase = DefaultRpcConsumer(queue_name)

    def _on_request(self, body: bytes):
        try:
            message = json.loads(body)
            # TODO: check that the function exist
            return_value = type(self).__dict__[message['func']](self, *message['args'], **message['kwargs'])
            return micropy_encode(json.dumps({'return_value': return_value}))
        except BaseException as e:
            raise_exception = e.__class__.__name__, traceback.format_exc()
            return micropy_encode(json.dumps({'raise_class': raise_exception}))

    def listen(self):
        self._broker.listen(self._on_request)
