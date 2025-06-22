from infrastructure.db.repositories import TaskRepository, TaskListRepository
from application.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
    TaskListCreate,
    TaskListUpdate,
    TaskListOut,
    TaskListFilteredResponse,
)
from application.schemas import TaskStatus


class TaskListUseCase:
    def __init__(self, list_repo: TaskListRepository, task_repo: TaskRepository):
        self.list_repo = list_repo
        self.task_repo = task_repo

    def create_list(self, data: TaskListCreate) -> TaskListOut:
        new_list = self.list_repo.create_list(name=data.name)
        return TaskListOut.model_validate(new_list)

    def update_list(self, list_id: int, data: TaskListUpdate) -> TaskListOut:
        task_list = self.list_repo.get_list(list_id)
        if data.name:
            task_list.name = data.name
        self.list_repo.db.commit()
        self.list_repo.db.refresh(task_list)
        return TaskListOut.model_validate(task_list)

    def get_list(self) -> list[TaskListOut]:
        return self.list_repo.get_all_lists()

    def delete_list(self, list_id: int):
        self.list_repo.delete_list(list_id)

    def list_tasks_with_completion(
        self, list_id: int, status: TaskStatus = None, priority=None
    ) -> TaskListFilteredResponse:
        """
        Get tasks from a given list, filtered by status and/or priority
        and returns them along with the completion percentage of the list.

        Args:
            list_id (int): The ID of the task list to query.
            status (TaskStatus, optional): Filter by task status. Defaults to None.
            priority (TaskPriority, optional): Filter by task priority. Defaults to None.

        Returns:
            TaskListFilteredResponse: A response containing the list of tasks
            and the completion percentage.
        """
        tasks = self.task_repo.get_tasks_by_list(list_id, status, priority)
        total = len(tasks)
        done = len(
            [
                each_task
                for each_task in tasks
                if each_task.status == TaskStatus.DONE.value
            ]
        )
        percentage = int((done / total) * 100) if total else 0
        return TaskListFilteredResponse(
            tasks=[TaskOut.model_validate(each_task) for each_task in tasks],
            completion=f"{percentage}%",
        )


class TaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, list_id: int, data: TaskCreate) -> TaskOut:
        task = self.repo.create_task(
            list_id=list_id,
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority,
        )
        return TaskOut.model_validate(task)

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
        return TaskOut.model_validate(task)

    def delete_task(self, task_id: int):
        self.repo.delete_task(task_id)

    def change_status(self, task_id: int, new_status: TaskStatus) -> TaskOut:
        task = self.repo.update_task_status(task_id, new_status)
        return TaskOut.model_validate(task)
