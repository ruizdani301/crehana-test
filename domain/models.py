from enum import Enum
from typing import List, Optional

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task:
    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str],
        status: TaskStatus,
        priority: TaskPriority,
        list_id: int,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.list_id = list_id

    def mark_done(self):
        self.status = TaskStatus.DONE


class TaskList:
    def __init__(self, id: int, name: str, tasks: Optional[List[Task]] = None):
        self.id = id
        self.name = name
        self.tasks = tasks or []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def completion_percentage(self) -> float:
        if not self.tasks:
            return 0.0
        done_tasks = sum(1 for t in self.tasks if t.status == TaskStatus.DONE)
        return (done_tasks / len(self.tasks)) * 100
