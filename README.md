# micropy
## Description:
`micropy` is a python packeage for creating and accessing micro service.

## Status:
`poc`

## Features:
- RPC
- More to come...

## Installation:
`pip install micropy` (currently from source code)

## Examples
### Client:
``` python
from micropy.client import micropy_rpc_client, micropy_rpc_catch
from examples.example_server_interface import BadInputException


@micropy_rpc_client(queue_name='example_server_queue')
class ExampleClient:

    @micropy_rpc_catch([BadInputException])
    def calc(self, x: int) -> int:
        pass


try:
    example_client = ExampleClient()
    print(example_client.calc(2))
    print(example_client.calc(0))
except BadInputException as e:
    print(e)

```

### Server:
``` python
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

```
