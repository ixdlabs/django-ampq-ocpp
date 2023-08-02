import json
import logging

import pika
import pika.exceptions
import time
from django.conf import settings
from pika.connection import URLParameters

logger = logging.getLogger(__name__)


class QueueConsumer:
    @staticmethod
    def consume(queue, fn):
        while True:
            try:
                logger.info("AMQP CONSUMER CONNECTING")
                connection = pika.BlockingConnection(URLParameters(settings.AMQP_URL))
                channel = connection.channel()
                channel.basic_qos(prefetch_count=1)
                channel.queue_declare(queue)

                def _callback(channel, method_frame, header_frame, body):
                    try:
                        fn(json.loads(body))
                    except Exception:
                        # TODO: identify cases where we might want to nack the message and have it re-deliver
                        logger.exception("AMQP MESSAGE")
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

                channel.basic_consume(queue, _callback)
                channel.start_consuming()
            except pika.exceptions.AMQPChannelError as e:
                logger.exception("AMQP CONSUMER")
                break
            except (
                pika.exceptions.ConnectionClosedByBroker,
                pika.exceptions.AMQPConnectionError,
            ):
                logger.exception("AMQP CONSUMER CONNECTION CLOSED")
                time.sleep(1)
                continue
