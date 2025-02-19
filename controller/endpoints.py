import threading

from fastapi import APIRouter
from starlette.responses import JSONResponse

from model.custom_request_object import CustomRequestObject
from service.direct_invocation_service import DirectInvocationService
from service.powershell_service import PowerShellService

router = APIRouter()


@router.get("/")
def read_root(custom_request_object: CustomRequestObject):
    th = threading.Thread(target=PowerShellService.handle_dispatch, args=(custom_request_object,),
                          daemon=True)
    th.start()
    return JSONResponse(
        content={
            "message": "Your request is being handled!",
        },
        status_code=200)


@router.get("/getGroup")
def get_group() -> JSONResponse:
    return JSONResponse(
        content={
            "message": "Hello, World!",
        },
        status_code=200)


@router.get("/dynamic/{path}")
def dynamic_path(path: str, custom_request_object: CustomRequestObject) -> JSONResponse:
    custom_request_object.add_action(path)
    th = threading.Thread(target=PowerShellService.handle_dispatch, args=(custom_request_object,),
                          daemon=True)
    th.start()
    return JSONResponse(
        content={
            "message": f"Your request is being handled! This is the {path} path",
            "order_id": f"{custom_request_object.order_id}",
            "action": f"{custom_request_object.action}"
        },
        status_code=200)


@router.get("/direct-invoke/{cmdlet}")
def direct_invoke(cmdlet: str) -> JSONResponse:
    """Invoke a PowerShell cmdlet asynchronously."""
    direct_invocation = DirectInvocationService(cmdlet)

    th = threading.Thread(target=direct_invocation.execute_cmdlet, daemon=True)
    th.start()

    return JSONResponse(
        content={
            "message": f"Your request is being handled! Cmdlet to be executed: {cmdlet}",
        },
        status_code=200
    )
