import threading

from fastapi import APIRouter
from starlette.responses import JSONResponse

from model.custom_request_object import CustomRequestObject
from service.powershell_service import PowerShellService

router = APIRouter()


@router.get("/")
def read_root(custom_request_object: CustomRequestObject):
    th = threading.Thread(target=PowerShellService.handle_dispatch, args=(custom_request_object, "getGroup"),
                          daemon=True)
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


@router.get("/dynamic/{path}")
def read_root(path: str, custom_request_object: CustomRequestObject) -> JSONResponse:
    custom_request_object.add_action(path)
    th = threading.Thread(target=PowerShellService.handle_dispatch, args=(custom_request_object, path),
                          daemon=True)
    th.start()
    return JSONResponse(
        content={
            "message": f"Your request is being handled! This is the {path} path",
            "order_id": f"{custom_request_object.order_id}",
            "action": f"{custom_request_object.action}"
        },
        status_code=200)
