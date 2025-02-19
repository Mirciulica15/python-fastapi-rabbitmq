from abc import ABC, abstractmethod

class RabbitMQConsumerInterface(ABC):
    """Interface for RabbitMQ consumers."""

    @abstractmethod
    def start_consuming(self):
        """Start consuming messages from RabbitMQ."""
        pass

    @abstractmethod
    def close(self):
        """Close the RabbitMQ connection."""
        pass
