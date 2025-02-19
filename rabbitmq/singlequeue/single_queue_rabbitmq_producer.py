import pika

from rabbitmq.rabbitmq_producer_interface import RabbitMQProducerInterface


class SingleQueueRabbitMQProducer(RabbitMQProducerInterface):
    def __init__(self, queue_name="demo_queue", host="localhost"):
        self.queue_name = queue_name
        self.host = host
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def publish(self, message: str, bank_id: str, user_id: str):
        self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=message.encode('utf-8'))

    def close(self):
        if self.connection:
            self.connection.close()
