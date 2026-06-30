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


def file_not_found_handler(request, exc: FileNotFoundError):
    logger.error(str(exc))

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": str(exc),
            "data": None,
            "error": "File Not Found",
        },
    )


def file_exists_handler(request, exc: FileExistsError):
    logger.error(str(exc))

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": str(exc),
            "data": None,
            "error": "File Already Exists",
        },
    )


def value_error_handler(request, exc: ValueError):
    logger.error(str(exc))

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
            "data": None,
            "error": "Invalid Request",
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
