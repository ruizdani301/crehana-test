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
    """
    Create a new task list.

    Args:
        data (TaskListCreate): The task list data to create.

    Returns:
        TaskListOut: The created task list.
        status: HTTP status code 200
    """
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
    """
    Retrieve all task lists.

    Args:
        db (Session): Database session (Dependency injection).
        current_user (dict): Authenticated user (Dependency injection).

    Returns:
        list[TaskListOut]: A list of all task lists.
        status: HTTP status code 200

    Raises:
        HTTPException (500): If there is an internal server error.
    """

    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return jsonable_encoder(use_case.get_list())


@router.put("/{list_id}", response_model=TaskListOut)
def update_task_list(
    list_id: int,
    data: TaskListUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    update a task list by its ID and with the provided data.

    Args:
        list_id (int): ID task list to update.
        data (TaskListUpdate): Datos a actualizar.

    Returns:
        TaskListOut: updated task list.
        status: HTTP status code 200

    Raises:
        HTTPException (404): if the task list doesn't exist.
        HTTPException (500): If there is an internal server error
    """
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return use_case.update_list(list_id, data)


@router.delete("/{list_id}")
def delete_task_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a task list by its ID.

    Args:
        list_id (int): The ID of the task list to delete.
        db (Session): Database session (Dependency injection).
        current_user (dict): Authenticated user (Dependency injection).

    Returns:
        dict: Confirmation message.
        status: HTTP status code 200

    Raises:
        HTTPException (404): If the task list doesn't exist or user lacks permission.
        HTTPException (500): If there is an internal server error
    """
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
    """
    Get tasks from a given list, filtered by status and/or priority
    and returns them along with the completion percentage of the list.

    Args:
        list_id (int): The ID of the task list to query.
        status (TaskStatus, optional): Filter by task status. Defaults to None.
        priority (str, optional): Filter by task priority. Defaults to None.

    Returns:
        TaskListFilteredResponse: A response containing the list of tasks
        and the completion percentage.
        HTTP status code 200
    """
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return use_case.list_tasks_with_completion(list_id, status, priority)


@router.post("/{list_id}/tasks", response_model=TaskOut)
def create_task(
    list_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new task in a task list.

    Args:
        list_id (int): ID of the task list to add the task to.
        data (TaskCreate): New task data to create.
        db (Session): Database session (Dependency injection).
        current_user (dict): Authenticated user (Dependency injection).

    Returns:
        TaskOut: Created task information.
        status: HTTP status code 200.

    Raises:
        HTTPException (404): If the task list doesn't exist or user lacks permission.
        HTTPException (422): If validation fails on the new task data.
        HTTPException (500): If there is an internal server error
    """
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
        status: HTTP status code 200

    Raises:
        HTTPException (404): If the task doesn't exist or user lacks permission.
        HTTPException (422): If validation fails on the update data.
        HTTPException (500): If there is an internal server error
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
        status: HTTP status code 200

    Raises:
        HTTPException (404): If the task does not exist or user lacks permission.
        HTTPException (400): If the status transition is invalid.
        HTTPException (500): If there is an internal server error
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
        HTTPException (500): If there is an internal server error
    """
    use_case = TaskUseCase(TaskRepository(db))
    use_case.delete_task(task_id)
    return {"message": "Task deleted"}
