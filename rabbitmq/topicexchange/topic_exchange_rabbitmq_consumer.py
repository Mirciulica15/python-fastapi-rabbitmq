import pika

from rabbitmq.rabbitmq_consumer_interface import RabbitMQConsumerInterface


class TopicExchangeRabbitMQConsumer(RabbitMQConsumerInterface):
    def __init__(self, bank_id: int, user_id: int, exchange_name="user_exchange", host="localhost"):
        self.bank_id = bank_id
        self.user_id = user_id
        self.exchange_name = exchange_name
        self.host = host
        self.connection = None
        self.channel = None
        self.queue_name = None
        self.connect()

    def connect(self):
        """Establish a RabbitMQ connection and declare a topic exchange."""
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="topic")

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.queue_name = result.method.queue

        routing_key = f"bank.{self.bank_id}.user.{self.user_id}"
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=routing_key)

        print(f" [*] Consumer waiting for messages on {routing_key}")

    def start_consuming(self):
        """Start consuming messages for this user."""

        def on_message(_, __, ___, body):
            print(f"Consumer received response from Rabbit MQ: {body.decode()}")

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=on_message, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        """Close the RabbitMQ connection."""
        if self.connection:
            self.connection.close()
