from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.jwt_handler import get_current_user
from infrastructure.db.repositories import TaskRepository, TaskListRepository
from application.use_cases.task_use_cases import TaskUseCase, TaskListUseCase
from application.schemas import (
    TaskCreate, TaskUpdate, TaskOut,
    TaskListCreate, TaskListUpdate, TaskListOut,
    TaskListFilteredResponse, TaskStatus
)
from infrastructure.db.database import get_db

router = APIRouter(prefix="/tasklists", tags=["Tareas"])


@router.post("/", response_model=TaskListOut)
def create_task_list(data: TaskListCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db),)
    return use_case.create_list(data)


@router.put("/{list_id}", response_model=TaskListOut)
def update_task_list(list_id: int, data: TaskListUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return use_case.update_list(list_id, data)


@router.delete("/{list_id}")
def delete_task_list(list_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    use_case.delete_list(list_id)
    return {"message": "Lista eliminada"}


@router.get("/{list_id}/tasks", response_model=TaskListFilteredResponse)
def list_tasks_with_filters(
    list_id: int,
    status: TaskStatus = None,
    priority: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    use_case = TaskListUseCase(TaskListRepository(db), TaskRepository(db))
    return use_case.list_tasks_with_completion(list_id, status, priority)



@router.post("/{list_id}/tasks", response_model=TaskOut)
def create_task(list_id: int, data: TaskCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    use_case = TaskUseCase(TaskRepository(db))
    return use_case.create_task(list_id, data)


@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    use_case = TaskUseCase(TaskRepository(db))
    return use_case.update_task(task_id, data)


@router.patch("/tasks/{task_id}/status", response_model=TaskOut)
def change_task_status(task_id: int, new_status: TaskStatus, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    use_case = TaskUseCase(TaskRepository(db))
    return use_case.change_status(task_id, new_status)


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    use_case = TaskUseCase(TaskRepository(db))
    use_case.delete_task(task_id)
    return {"message": "Tarea eliminada"}
