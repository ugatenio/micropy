from micropy.server import MicropyRpcProducer
from examples.example_server_interface import BadInputException


class ExampleService(MicropyRpcProducer):

    def __init__(self):
        super().__init__(queue_name='example_server_queue')
        self._exp = 2

    def calc(self, x: int) -> int:
        if not x:
            raise BadInputException('it\'s obvious')
        return x ** self._exp


ExampleService().listen()
