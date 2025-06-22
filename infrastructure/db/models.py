from application.schemas import TaskStatus, TaskPriority
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from infrastructure.db.database import Base

# Base = declarative_base()


# class TaskStatus(str, enum.Enum):
#     pending = "pending"
#     in_progress = "in_progress"
#     done = "done"


# class TaskPriority(str, enum.Enum):
#     low = "low"
#     medium = "medium"
#     high = "high"


class TaskListModel(Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    tasks = relationship(
        "TaskModel", back_populates="task_list", cascade="all, delete-orphan"
    )


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium)

    list_id = Column(Integer, ForeignKey("task_lists.id"))

    # Relación inversa con la lista
    task_list = relationship("TaskListModel", back_populates="tasks")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(500), nullable=False)
