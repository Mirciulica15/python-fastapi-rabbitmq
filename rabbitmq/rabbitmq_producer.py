import json

import pika


class RabbitMQProducer:
    def __init__(self, queue_name="demo_queue", host="localhost"):
        self.queue_name = queue_name
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def publish(self, message: dict):
        message_str = json.dumps(message)
        self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=message_str.encode('utf-8'))

    def close(self):
        self.connection.close()
