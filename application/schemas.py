from pydantic import BaseModel, Field, field_validator
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
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The title must be between 1 and 100 characters.",
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Description (máx. 500 caracteres).",
    )
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        description="Task status (pending, in_progress, completed).",
    )
    priority: TaskPriority = Field(
        default=TaskPriority.medium, description="Task priority (low, medium, high)."
    )


@field_validator("title")
def validate_title(cls, value) -> str:
    if value.strip() == "":
        raise ValueError("The title cannot be empty or contain only spaces.")
    return value


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

    model_config = {"from_attributes": True}


class TaskListCreate(BaseModel):
    name: str


class TaskListUpdate(BaseModel):
    name: Optional[str]


class TaskListOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


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
