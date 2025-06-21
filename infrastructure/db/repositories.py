from sqlalchemy.orm import Session
from infrastructure.db.models import TaskModel, TaskListModel
from domain.models import TaskStatus, TaskPriority  # si compartes enums, opcional

# Repositorio para listas de tareas
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

    def delete_list(self, list_id: int):
        task_list = self.get_list(list_id)
        if task_list:
            self.db.delete(task_list)
            self.db.commit()

# Repositorio para tareas
class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, list_id: int, title: str, description: str, status: TaskStatus, priority: TaskPriority) -> TaskModel:
        task = TaskModel(
            list_id=list_id,
            title=title,
            description=description,
            status=status,
            priority=priority
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> TaskModel:
        return self.db.query(TaskModel).filter_by(id=task_id).first()

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

    def get_tasks_by_list(self, list_id: int, status: TaskStatus = None, priority: TaskPriority = None) -> list[TaskModel]:
        query = self.db.query(TaskModel).filter(TaskModel.list_id == list_id)
        if status:
            query = query.filter(TaskModel.status == status)
        if priority:
            query = query.filter(TaskModel.priority == priority)
        return query.all()
