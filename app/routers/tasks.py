from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.task import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])

tasks_db: dict[int, dict] = {}


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):

    id = len(tasks_db) + 1
    status = "pending"
    created_at = datetime.now(tz=timezone.utc)

    task_data = task.model_dump()

    task_record = {**task_data, "id": id, "status": status, "created_at": created_at}

    tasks_db[id] = task_record

    return task_record


@router.get("/", response_model=list[TaskRead], status_code=status.HTTP_200_OK)
async def get_tasks(status: Optional[str] = Query(default=None)):

    if not status:
        tasks = list(tasks_db.values())
        return tasks

    tasks_filtered = [t for t in tasks_db.values() if t.get("status") == status]

    return tasks_filtered


@router.get("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int):

    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=" Task ID not informed !"
        )

    try:
        task_by_id = tasks_db[task_id]
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=" Task ID not found !"
        )

    return task_by_id
