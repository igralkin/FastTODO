from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    datetime_to_do: datetime
    task_info: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    datetime_to_do: Optional[datetime] = None
    task_info: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)