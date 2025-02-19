import json
from datetime import datetime, timezone

import requests

from model.request_object import RequestObject
from service.rabbitmq_service import RabbitMQService


def handle_dispatch(request_object: RequestObject, action: str) -> None:
    print("Handle dispatch thread started!", datetime.now(timezone.utc))
    bank_id = "8813"
    user_id = "mircea"
    request_object.add_action(action)
    response = requests.get(
        url="http://localhost:8000/test",
    )

    message_str = (
            str(response.status_code) + " " +
            json.dumps(response.json()) +
            " at time " +
            str(datetime.now(timezone.utc)) +
            " from bank " +
            bank_id +
            " and user " +
            user_id
    )
    print("Producer published response to Rabbit MQ: ", message_str)
    RabbitMQService.get_instance().get_producer().publish(message=message_str, bank_id="8813", user_id="mircea")
