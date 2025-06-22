import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, ANY
from main import app

client = TestClient(app)


@pytest.fixture
def mock_user_repo(monkeypatch):
    mock = MagicMock()

    mock.get_user_by_username.return_value = None

    mock.create_user.return_value = None

    monkeypatch.setattr(
        "infrastructure.db.user_repository.get_user_by_username",
        mock.get_user_by_username,
    )
    monkeypatch.setattr(
        "infrastructure.db.user_repository.create_user", mock.create_user
    )

    return mock


def test_register_user_success(mock_user_repo):
    payload = {"username": "nuevo_usuario", "password": "clave123"}

    response = client.post("/users/register", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "user created successfully"}

    mock_user_repo.get_user_by_username.assert_called_once_with(ANY, "nuevo_usuario")
    mock_user_repo.create_user.assert_called_once_with(ANY, "nuevo_usuario", "clave123")
