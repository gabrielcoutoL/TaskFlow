from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi import status as http_status

from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

tasks_db: dict[int, dict] = {}
_next_id: int = 1


@router.post("/", response_model=TaskRead, status_code=http_status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    global _next_id

    task_record = {
        **task.model_dump(),
        "id": _next_id,
        "status": "pending",
        "created_at": datetime.now(tz=timezone.utc),
    }

    tasks_db[_next_id] = task_record
    _next_id += 1

    return task_record


@router.get("/", response_model=list[TaskRead], status_code=http_status.HTTP_200_OK)
async def get_tasks(task_status: Optional[str] = Query(default=None)):
    tasks = list(tasks_db.values())

    if task_status:
        tasks = [t for t in tasks if t.get("status") == task_status]

    return tasks


@router.get("/{task_id}", response_model=TaskRead, status_code=http_status.HTTP_200_OK)
async def get_task_by_id(task_id: int):
    task = tasks_db.get(task_id)

    if not task:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Task não encontrada",
        )

    return task


@router.patch(
    "/{task_id}", response_model=TaskRead, status_code=http_status.HTTP_200_OK
)
async def update_task(task_id: int, task_update: TaskUpdate):
    task = tasks_db.get(task_id)

    if not task:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Task não encontrada",
        )

    update_data = task_update.model_dump(exclude_unset=True)
    task.update(update_data)

    return task


@router.delete("/{task_id}", status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    task = tasks_db.get(task_id)

    if not task:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Task não encontrada",
        )

    tasks_db.pop(task_id)
