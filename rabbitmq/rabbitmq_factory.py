from rabbitmq.rabbitmq_consumer_interface import RabbitMQConsumerInterface
from rabbitmq.rabbitmq_producer_interface import RabbitMQProducerInterface
from rabbitmq.singlequeue.single_queue_rabbitmq_consumer import SingleQueueRabbitMQConsumer
from rabbitmq.singlequeue.single_queue_rabbitmq_producer import SingleQueueRabbitMQProducer
from rabbitmq.topicexchange.topic_exchange_rabbitmq_consumer import TopicExchangeRabbitMQConsumer
from rabbitmq.topicexchange.topic_exchange_rabbitmq_producer import TopicExchangeRabbitMQProducer


class RabbitMQFactory:
    """Factory to create a producer or consumer."""

    @staticmethod
    def get_producer(strategy_type: str, **kwargs) -> RabbitMQProducerInterface:
        """Returns a producer instance based on the strategy type."""
        if strategy_type == "single_queue":
            return SingleQueueRabbitMQProducer(**kwargs)
        elif strategy_type == "topic_exchange":
            return TopicExchangeRabbitMQProducer(**kwargs)
        else:
            raise ValueError("Invalid strategy type for producer. Choose 'single_queue' or 'topic_exchange'.")

    @staticmethod
    def get_consumer(strategy_type: str, **kwargs) -> RabbitMQConsumerInterface:
        """Returns a consumer instance based on the strategy type."""
        if strategy_type == "single_queue":
            return SingleQueueRabbitMQConsumer(**kwargs)
        elif strategy_type == "topic_exchange":
            return TopicExchangeRabbitMQConsumer(**kwargs)
        else:
            raise ValueError("Invalid strategy type for consumer. Choose 'single_queue' or 'topic_exchange'.")
