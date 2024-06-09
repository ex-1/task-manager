from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.types import TIMESTAMP


class ProjectBase(BaseModel):
    name: str
    description: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    name: str
    status: str
    time_in_status: datetime = datetime.now().replace(tzinfo=None)
    start_at: datetime = datetime.now().replace(tzinfo=None)
    deadline: datetime = datetime.now().replace(tzinfo=None)
    end_at: datetime = datetime.now().replace(tzinfo=None)
    timer_task: timedelta | None = None
    performer_id: int | None = None
    project_id: int
    parent_task_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True
