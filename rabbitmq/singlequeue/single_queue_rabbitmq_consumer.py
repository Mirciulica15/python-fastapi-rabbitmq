import pika

from rabbitmq.rabbitmq_consumer_interface import RabbitMQConsumerInterface


class SingleQueueRabbitMQConsumer(RabbitMQConsumerInterface):
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

    def start_consuming(self):
        def on_message(_, __, ___, body):
            print(f"Consumer received response from Rabbit MQ: {body.decode()}")

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=on_message, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        if self.connection:
            self.connection.close()
