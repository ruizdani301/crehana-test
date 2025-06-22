from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from infrastructure.db.models import TaskModel, TaskListModel
from application.schemas import TaskListOut, TaskStatus, TaskPriority


# TaskList repository
class TaskListRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_list(self, name: str) -> TaskListModel:
        task_list = TaskListModel(name=name)
        self.db.add(task_list)
        self.db.commit()
        self.db.refresh(task_list)
        return task_list

    def get_list(self, list_id: int) -> TaskListModel:
        return self.db.query(TaskListModel).filter_by(id=list_id).first()

    def get_all_lists(self) -> list[TaskListOut]:
        db_lists = self.db.query(TaskListModel).all()
        return [TaskListOut.model_validate(db_list) for db_list in db_lists]

    def delete_list(self, list_id: int):
        task_list = self.get_list(list_id)
        if task_list:
            self.db.delete(task_list)
            self.db.commit()


# Task repository
class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_task(
        self,
        list_id: int,
        title: str,
        description: str,
        status: TaskStatus,
        priority: TaskPriority,
    ) -> TaskModel:
        task = TaskModel(
            list_id=list_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> TaskModel:
        try:
            task = self.db.query(TaskModel).filter_by(id=task_id).first()

            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task with ID {task_id} not found",
                )

            return task

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def update_task_status(self, task_id: int, new_status: TaskStatus) -> TaskModel:
        task = self.get_task(task_id)
        if task:
            task.status = new_status
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.get_task(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()

    def get_tasks_by_list(
        self,
        list_id: int,
        status_task: TaskStatus = None,
        priority: TaskPriority = None,
    ) -> list[TaskModel]:
        try:
            if list_id <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The ID should be a positive integer.",
                )

            query = self.db.query(TaskModel).filter(TaskModel.list_id == list_id)
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"List with ID {list_id} not found",
                )
            if status_task:
                query = query.filter(TaskModel.status == status_task)
            if priority:
                query = query.filter(TaskModel.priority == priority)
            return query.all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al consultar tareas: {str(e)}",
            )
