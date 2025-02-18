import pika


class RabbitMQConsumer:
    def __init__(self, queue_name="demo_queue", host="localhost"):
        self.queue_name = queue_name
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def on_message(self, channel, method, properties, body):
        print(f"Consumer received event: {body.decode()}")

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message, auto_ack=True)
        self.channel.start_consuming()
