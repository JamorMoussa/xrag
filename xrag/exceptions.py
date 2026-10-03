from fastapi import Request
from fastapi.responses import JSONResponse


class XRAGException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        code: str = "internal_error",
    ):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class DocumentNotFoundError(XRAGException):
    def __init__(self, key: str):
        super().__init__(
            message=f"Document key='{key}' not found.",
            status_code=404,
            code="document_not_found",
        )


async def xrag_exception_handler(
    request: Request,
    exc: XRAGException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )