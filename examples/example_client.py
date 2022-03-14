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
