from abc import ABC, abstractmethod


class RabbitMQProducerInterface(ABC):
    """Interface for RabbitMQ producers."""

    @abstractmethod
    def publish(self, message: str, bank_id: str, user_id: str):
        """Send a message to RabbitMQ with bank_id and user_id."""
        pass

    @abstractmethod
    def close(self):
        """Close the RabbitMQ connection."""
        pass
