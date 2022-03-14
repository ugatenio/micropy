import uuid
from typing import Callable

import pika

from micropy.brokers.base import MicropyRpcConsumerBase, MicropyRpcProducerBase


class RabbitRpcProducer(MicropyRpcProducerBase):

    def __init__(self, queue_name: str):
        super().__init__(queue_name)
        credentials = pika.PlainCredentials(username='admin', password='admin')
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', credentials=credentials)
        )
        self._channel = self._connection.channel()
        self._callback_queue = self._channel.queue_declare(queue='', exclusive=True).method.queue
        self._channel.basic_consume(queue=self._callback_queue, on_message_callback=self._on_response, auto_ack=True)
        self._corr_id = None
        self._is_response_arrived = False
        self._response_data = bytes()

    def rcp_call(self, message: bytes) -> bytes:
        self._corr_id = str(uuid.uuid4())
        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue_name,
            properties=pika.BasicProperties(reply_to=self._callback_queue, correlation_id=self._corr_id),
            body=message
        )
        self._wait_for_response()
        return self._response_data

    def _wait_for_response(self) -> None:
        self._is_response_arrived = False
        while self._is_response_arrived is not True:
            self._connection.process_data_events()

    # pylint: disable=unused-arguments
    def _on_response(self, ch, method, props, body) -> None:
        if self._corr_id == props.correlation_id:
            self._is_response_arrived = True
            self._response_data = body


class RabbitRpcConsumer(MicropyRpcConsumerBase):

    def __init__(self, queue_name: str):
        super().__init__(queue_name)
        credentials = pika.PlainCredentials(username='admin', password='admin')
        self._channel = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', credentials=credentials)
        ).channel()

    def listen(self, request_handler: Callable) -> None:
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=lambda ch, method, props, body: self._on_request(
                ch, method, props, body, request_handler
            )
        )
        self._channel.start_consuming()

    def _on_request(self, ch, method, props, body, request_handler: Callable):
        response = request_handler(body)
        self._channel.basic_publish(exchange='',
                                    routing_key=props.reply_to,
                                    properties=pika.BasicProperties(correlation_id=props.correlation_id),
                                    body=response)
        self._channel.basic_ack(delivery_tag=method.delivery_tag)

