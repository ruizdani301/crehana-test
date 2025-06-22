from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from utils.jwt_handler import get_current_user
from infrastructure.db.repositories import TaskRepository, TaskListRepository
from application.use_cases.task_use_cases import TaskUseCase, TaskListUseCase
from application.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
    TaskListCreate,
    TaskListUpdate,
    TaskListOut,
    TaskListFilteredResponse,
    TaskStatus,
)
from infrastructure.db.database import get_db

router = APIRouter(prefix="/tasklists", tags=["Tareas"])


@router.post("/", response_model=TaskListOut)
def create_task_list(
    data: TaskListCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    use_case = TaskListUseCase(
        TaskListRepository(db),
        TaskRepository(db),
    )
    return use_case.create_list(data)


@router.get("/get_all", response_model=list[TaskListOut])
def get_task_list(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return jsonable_encoder(use_case.get_list())


@router.put("/{list_id}", response_model=TaskListOut)
def update_task_list(
    list_id: int,
    data: TaskListUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return use_case.update_list(list_id, data)


@router.delete("/{list_id}")
def delete_task_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    use_case.delete_list(list_id)
    return {"message": "List deleted"}


@router.get("/{list_id}/tasks", response_model=TaskListFilteredResponse)
def list_tasks_with_filters(
    list_id: int,
    status: TaskStatus = None,
    priority: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return use_case.list_tasks_with_completion(list_id, status, priority)


@router.post("/{list_id}/tasks", response_model=TaskOut)
def create_task(
    list_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    use_case = TaskUseCase(TaskRepository(db))
    return use_case.create_task(list_id, data)


@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update an existing task.

    Args:
        task_id (int): ID of the task to update.
        data (TaskUpdate): New task data to apply.
        db (Session): Database session (Dependency injection).
        current_user (dict): Authenticated user (Dependency injection).

    Returns:
        TaskOut: Updated task information.

    Raises:
        HTTPException (404): If the task doesn't exist or user lacks permission.
        HTTPException (422): If validation fails on the update data.
    """
    use_case = TaskUseCase(TaskRepository(db))
    return use_case.update_task(task_id, data)


@router.patch("/tasks/{task_id}/status", response_model=TaskOut)
def change_task_status(
    task_id: int,
    new_status: TaskStatus,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update the status of a task.

    Args:
        task_id (int): ID of the task to update.
        new_status (TaskStatus): New status to assign to the task.
        db (Session): Database session (Dependency injection).
        current_user (dict): Authenticated user (Dependency injection).

    Returns:
        TaskOut: Updated task data.

    Raises:
        HTTPException (404): If the task does not exist or user lacks permission.
        HTTPException (400): If the status transition is invalid.
    """
    use_case = TaskUseCase(TaskRepository(db))
    return use_case.change_status(task_id, new_status)


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a task by its ID.

    Args:
        task_id (int): ID of the task to delete.
        db (Session): Database session (Dependency injection).
        current_user (dict): Authenticated user (Dependency injection).

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException (404): If the task does not exist or user lacks permission.
    """
    use_case = TaskUseCase(TaskRepository(db))
    use_case.delete_task(task_id)
    return {"message": "Task deleted"}
