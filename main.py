import threading

from fastapi import FastAPI
from starlette.responses import JSONResponse

from model.custom_request_object import CustomRequestObject
from service.powershell_service import handle_dispatch
from service.rabbitmq_service import RabbitMQService

app = FastAPI()


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
    rabbitmq_service = RabbitMQService.get_instance()
    rabbitmq_service.start_rabbitmq_service()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
