from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"



class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    list_id: int

    model_config = {
        "from_attributes": True
    }



class TaskListCreate(BaseModel):
    name: str


class TaskListUpdate(BaseModel):
    name: Optional[str]


class TaskListOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class TaskListFilteredResponse(BaseModel):
    tasks: List[TaskOut]
    completion: str


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class CreatedUser(BaseModel):
    message: str