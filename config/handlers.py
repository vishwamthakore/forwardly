from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI
from config.exceptions import AppException
from fastapi.exceptions import RequestValidationError
import traceback


def add_all_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.__class__.__name__,
            "message": exc.message,
            "status_code": exc.status_code,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    # log real error internally
    print(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "InternalServerError",
            "message": "Something went wrong",
            "status_code": 500,
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "ValidationError",
            "message": "Invalid request",
            "details": exc.errors(),
            "status_code": 422,
        },
    )