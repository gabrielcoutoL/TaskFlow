from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    created_at: datetime


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    id: Optional[int]
    status: Optional[str]
    created_at: Optional[datetime]
