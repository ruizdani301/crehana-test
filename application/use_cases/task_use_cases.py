from infrastructure.db.repositories import TaskRepository, TaskListRepository
from application.schemas import (
    TaskCreate, TaskUpdate, TaskOut,
    TaskListCreate, TaskListUpdate, TaskListOut, TaskListFilteredResponse
)
from domain.models import TaskStatus

class TaskListUseCase:
    def __init__(self, list_repo: TaskListRepository, task_repo: TaskRepository):
        self.list_repo = list_repo
        self.task_repo = task_repo

    def create_list(self, data: TaskListCreate) -> TaskListOut:
        new_list = self.list_repo.create_list(name=data.name)
        return TaskListOut.from_orm(new_list)

    def update_list(self, list_id: int, data: TaskListUpdate) -> TaskListOut:
        task_list = self.list_repo.get_list(list_id)
        if data.name:
            task_list.name = data.name
        self.list_repo.db.commit()
        self.list_repo.db.refresh(task_list)
        return TaskListOut.from_orm(task_list)

    def delete_list(self, list_id: int):
        self.list_repo.delete_list(list_id)

    def list_tasks_with_completion(self, list_id: int, status: TaskStatus = None, priority=None) -> TaskListFilteredResponse:
        tasks = self.task_repo.get_tasks_by_list(list_id, status, priority)
        total = len(tasks)
        done = len([t for t in tasks if t.status == TaskStatus.DONE.value])
        print(done)
        percentage = int((done / total) * 100) if total else 0
        return TaskListFilteredResponse(tasks=[TaskOut.from_orm(t) for t in tasks], completion=f"{percentage}%")


class TaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, list_id: int, data: TaskCreate) -> TaskOut:
        task = self.repo.create_task(
            list_id=list_id,
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority
        )
        return TaskOut.from_orm(task)

    def update_task(self, task_id: int, data: TaskUpdate) -> TaskOut:
        task = self.repo.get_task(task_id)
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status
        if data.priority is not None:
            task.priority = data.priority
        self.repo.db.commit()
        self.repo.db.refresh(task)
        return TaskOut.from_orm(task)

    def delete_task(self, task_id: int):
        self.repo.delete_task(task_id)

    def change_status(self, task_id: int, new_status: TaskStatus) -> TaskOut:
        task = self.repo.update_task_status(task_id, new_status)
        return TaskOut.from_orm(task)
