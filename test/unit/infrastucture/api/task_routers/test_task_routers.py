import pytest
from unittest.mock import MagicMock
from main import app
from application.schemas import TaskListCreate, TaskListUpdate, TaskCreate, TaskUpdate, TaskStatus
from fastapi.testclient import TestClient
from utils.jwt_handler import get_current_user
from application.use_cases.task_use_cases import TaskUseCase, TaskListOut
from infrastructure.api.task_routes import (
    create_task_list,
    get_task_list,
    update_task_list,
    delete_task_list,
    list_tasks_with_filters,
    create_task,
    update_task,
    change_task_status,
    delete_task,
)



app.dependency_overrides[get_current_user] = lambda: {"user_id": 1}

@pytest.fixture
def mock_use_case(monkeypatch):
    mock = MagicMock()
    mock.get_list.return_value = [
        TaskListOut(id=1, name="Lista 1"),
        TaskListOut(id=2, name="Lista 2"),
    ]
    monkeypatch.setattr(
        "application.use_cases.task_use_cases.TaskListUseCase",
        lambda *args, **kwargs: mock
    )
    return mock

client = TestClient(app)

def test_get_all_lists_returns_tasklistout(mock_use_case):
    try:
        response = client.get("/tasklists/get_all")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert data[0]["id"] == 1
        assert data[0]["name"] == "hogar"
        assert data[1]["id"] == 2
        assert data[1]["name"] == "oficina"
    finally:
        app.dependency_overrides = {}
