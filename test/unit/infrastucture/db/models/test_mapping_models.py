from infrastructure.db.models import TaskListModel, TaskModel, UserModel, TaskStatus, TaskPriority

def test_tasklist_model_basic():
    tasklist = TaskListModel(name="Lista prueba")
    assert tasklist.name == "Lista prueba"
    assert hasattr(tasklist, "tasks")
    assert isinstance(tasklist.tasks, list) or tasklist.tasks is None

def test_task_model_basic_relations():
    tasklist = TaskListModel(name="Lista prueba")
    task = TaskModel(title="Tarea 1", task_list=tasklist)
    
    assert task.task_list == tasklist
    assert task.title == "Tarea 1"
    
   
    tasklist.tasks = [task]
    assert tasklist.tasks[0] == task

def test_task_model_default_enum_values():
    task = TaskModel(title="Tarea enum", status=TaskStatus.pending, priority=TaskPriority.medium)
    assert task.status == TaskStatus.pending
    assert task.priority == TaskPriority.medium


def test_user_model_basic():
    user = UserModel(username="usuario1", password_hash="hash123")
    assert user.username == "usuario1"
    assert user.password_hash == "hash123"


def test_tasklist_can_hold_tasks():
    tasklist = TaskListModel(name="Lista hogar")
    task1 = TaskModel(title="Lavar platos")
    task2 = TaskModel(title="Hacer mercado")

    # Simular la asignación manual (no automática sin DB)
    task1.task_list = tasklist
    task2.task_list = tasklist
    tasklist.tasks = [task1, task2]

    assert task1.task_list == tasklist
    assert task2.task_list == tasklist
    assert len(tasklist.tasks) == 2
    assert tasklist.tasks[0].title == "Lavar platos"


def test_create_user_model():
    user = UserModel(username="usuario_test", password_hash="hashed_pw")
    assert user.username == "usuario_test"
    assert user.password_hash == "hashed_pw"


def test_task_status_enum_values():
    assert TaskStatus.pending.value == "pending"
    assert TaskStatus.done.value == "done"

def test_task_priority_enum_values():
    values = [p.value for p in TaskPriority]
    assert "low" in values
    assert "medium" in values
    assert "high" in values
