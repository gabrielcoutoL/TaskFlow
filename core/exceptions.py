from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Formato padronizado para todos os erros HTTP da API."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Formato padronizado para erros de validação do Pydantic."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Erro de validação nos dados enviados",
            "status_code": 422,
            "details": exc.errors(),
        },
    )
