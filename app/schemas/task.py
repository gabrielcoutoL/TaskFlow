from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    created_at: datetime


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None
