import pika

from rabbitmq.rabbitmq_producer_interface import RabbitMQProducerInterface


class TopicExchangeRabbitMQProducer(RabbitMQProducerInterface):
    def __init__(self, exchange_name="user_exchange", host="localhost"):
        self.exchange_name = exchange_name
        self.host = host
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Establish a RabbitMQ connection and declare a topic exchange."""
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="topic")

    def publish(self, message: str, bank_id: str, user_id: str):
        """Publish a message with a routing key using the topic exchange."""
        routing_key = f"bank.{bank_id}.user.{user_id}"
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=routing_key,
            body=message.encode("utf-8")
        )

    def close(self):
        """Close the RabbitMQ connection."""
        if self.connection:
            self.connection.close()
