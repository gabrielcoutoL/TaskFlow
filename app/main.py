from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from app.routers.tasks import router as tasks_router
from core.exceptions import http_exception_handler, validation_exception_handler

tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operações de CRUD das Tasks",
    }
]

app = FastAPI(
    title="TaskFlow API",
    version="0.1.0",
    description="Projeto desenvolvido para prática simulando um app de gerenciamento de tarefas",
    openapi_tags=tags_metadata,
)


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


app.include_router(tasks_router)
