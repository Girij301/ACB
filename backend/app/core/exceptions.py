from app.core.logger import logger
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, message: str):
        self.message = message


def app_exception_handler(request, exc: AppException):
    logger.error(f"AppException: {exc.message}")

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Application Error",
            "data": None,
            "error": exc.message,
        },
    )


def generic_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled Error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "data": None,
            "error": str(exc),
        },
    )
