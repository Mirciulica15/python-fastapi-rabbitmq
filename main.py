from fastapi import FastAPI

from controller.endpoints import router
from service.rabbitmq_service import RabbitMQService

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    rabbitmq_service = RabbitMQService.get_instance()
    rabbitmq_service.start_rabbitmq_service()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
