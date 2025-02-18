import threading

from fastapi import FastAPI
from starlette.responses import JSONResponse

from model.custom_request_object import CustomRequestObject
from rabbitmq.rabbitmq_consumer import RabbitMQConsumer
from rabbitmq.rabbitmq_producer import RabbitMQProducer
from service.powershell_service import handle_dispatch

rabbitmq_producer: RabbitMQProducer = RabbitMQProducer(queue_name="demo_queue", host="localhost")
rabbitmq_consumer: RabbitMQConsumer = RabbitMQConsumer(queue_name="demo_queue", host="localhost")
app = FastAPI()


def start_rabbitmq_consumer():
    rabbitmq_consumer.start_consuming()


thread = threading.Thread(target=start_rabbitmq_consumer, daemon=True)
thread.start()


@app.get("/")
def read_root(custom_request_object: CustomRequestObject):
    th = threading.Thread(target=handle_dispatch, args=(custom_request_object, "getGroup"), daemon=True)
    th.start()
    return JSONResponse(
        content={
            "message": "Your request is being handled!",
        },
        status_code=200)


@app.get("/test")
def read_root() -> JSONResponse:
    return JSONResponse(
        content={
            "message": "Hello, World!",
        },
        status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
