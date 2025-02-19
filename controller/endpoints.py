import threading

from fastapi import APIRouter
from starlette.responses import JSONResponse

from model.custom_request_object import CustomRequestObject
from service.powershell_service import handle_dispatch

router = APIRouter()


@router.get("/")
def read_root(custom_request_object: CustomRequestObject):
    th = threading.Thread(target=handle_dispatch, args=(custom_request_object, "getGroup"), daemon=True)
    th.start()
    return JSONResponse(
        content={
            "message": "Your request is being handled!",
        },
        status_code=200)


@router.get("/test")
def read_root() -> JSONResponse:
    return JSONResponse(
        content={
            "message": "Hello, World!",
        },
        status_code=200)
