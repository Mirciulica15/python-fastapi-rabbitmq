from datetime import datetime, timezone

import requests

from model.request_object import RequestObject


def handle_dispatch(request_object: RequestObject, action: str) -> None:
    from main import rabbitmq_producer
    print("Handle dispatch thread started!", datetime.now(timezone.utc))
    request_object.add_action(action)
    response = requests.get(
        url="http://localhost:8000/test",
    )

    print(
        "Producer publishes the response to Rabbit MQ: ",
        response.status_code,
        response.json(),
        " at time: ",
        datetime.now(timezone.utc)
    )
    rabbitmq_producer.publish(message=response.json())
