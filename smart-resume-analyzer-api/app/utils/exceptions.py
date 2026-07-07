from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.logger import logger


class ApplicationException(Exception):

    def __init__(self, message: str):
        self.message = message


async def application_exception_handler(
    request: Request,
    exc: ApplicationException
):

    logger.error(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Ha ocurrido un error interno."
        }
    )