import os
import threading

from dotenv import load_dotenv

from rabbitmq.rabbitmq_factory import RabbitMQFactory
from rabbitmq.rabbitmq_producer_interface import RabbitMQProducerInterface


class RabbitMQService:
    """Service for configuring and managing RabbitMQ consumer and producer based on the strategy type."""

    # Class-level variable for the singleton instance
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of RabbitMQService is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initialize the RabbitMQService instance."""
        if not hasattr(self, '_initialized'):  # Check if already initialized
            self._rabbitmq_producer: RabbitMQProducerInterface = None
            self._rabbitmq_consumer = None
            load_dotenv()
            self._initialized = True  # Set initialized flag to True to avoid re-initialization

    @staticmethod
    def get_strategy_type():
        """Get the strategy type from environment variable."""
        return os.getenv("STRATEGY_TYPE", "single_queue").strip().lower()

    def start_rabbitmq_service(self):
        """Start RabbitMQ consumer and producer based on the strategy type."""
        strategy_type = self.get_strategy_type()

        producer_kwargs = self._get_producer_kwargs(strategy_type)
        consumer_kwargs = self._get_consumer_kwargs(strategy_type)

        self._rabbitmq_producer = RabbitMQFactory.get_producer(strategy_type, **producer_kwargs)
        self._rabbitmq_consumer = RabbitMQFactory.get_consumer(strategy_type, **consumer_kwargs)

        consumer_thread = threading.Thread(target=self._rabbitmq_consumer.start_consuming, daemon=True)
        consumer_thread.start()

    @staticmethod
    def _get_producer_kwargs(strategy_type):
        """Prepare producer-specific kwargs based on strategy."""
        if strategy_type == "single_queue":
            queue_name = os.getenv("QUEUE_NAME", "demo_queue")
            return {"queue_name": queue_name}
        elif strategy_type == "topic_exchange":
            exchange_name = os.getenv("EXCHANGE_NAME", "user_exchange")
            host = os.getenv("RABBITMQ_HOST", "localhost")
            return {"exchange_name": exchange_name, "host": host}

    @staticmethod
    def _get_consumer_kwargs(strategy_type):
        """Prepare consumer-specific kwargs based on strategy."""
        if strategy_type == "single_queue":
            queue_name = os.getenv("QUEUE_NAME", "demo_queue")
            return {"queue_name": queue_name}
        elif strategy_type == "topic_exchange":
            exchange_name = os.getenv("EXCHANGE_NAME", "user_exchange")
            bank_id = str(os.getenv("BANK_ID", "8813"))
            user_id = str(os.getenv("USER_ID", "mircea"))
            return {"exchange_name": exchange_name, "bank_id": bank_id, "user_id": user_id}

    def get_producer(self):
        """Return the appropriate producer based on the strategy type."""
        return self._rabbitmq_producer

    @classmethod
    def get_instance(cls):
        """Returns the singleton instance of RabbitMQService."""
        if cls._instance is None:
            cls._instance = RabbitMQService()  # Create the instance if it doesn't exist
        return cls._instance
