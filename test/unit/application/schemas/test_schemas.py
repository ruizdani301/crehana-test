import pytest
from application.schemas import (
    TaskCreate,
    TaskStatus,
    TaskPriority,
    TaskOut,
    UserCreate,
    Token,
)
from pydantic import ValidationError


def test_task_create_valid():
    task = TaskCreate(
        title="clean house",
        description="need to clean house",
        status=TaskStatus.pending,
        priority=TaskPriority.high,
    )
    assert task.title == "clean house"
    assert task.status == "pending"


@pytest.mark.parametrize(
    "title,should_raise",
    [("m" * 100, False), ("m" * 101, True), (" " * 100 + "m", True)],
)
def test_title_length_validation(title, should_raise):
    """test that the title length is validated"""
    if should_raise:
        with pytest.raises(ValidationError):
            TaskCreate(title=title, description="invalid description")
    else:
        task = TaskCreate(title=title, description="valid description")
        assert len(task.title) <= 100


@pytest.mark.parametrize(
    "invalid_priority, expected_msg",
    [
        (2, "Input should be 'low', 'medium' or 'high'"),
        ("invalid", "Input should be 'low', 'medium' or 'high'"),
        (None, "Input should be 'low', 'medium' or 'high'"),
    ],
)
def test_task_out_invalid_priority(invalid_priority, expected_msg):
    with pytest.raises(ValidationError) as exc_info:
        TaskOut(
            priority=invalid_priority,
            status=TaskStatus.pending,
            title="title",
            description="description",
            id=1,
            list_id=1,
        )

    errors = exc_info.value.errors()
    assert any(expected_msg in error["msg"] for error in errors)


def test_user_create():
    user = UserCreate(username="testuser", password="secret")
    assert user.username == "testuser"


def test_token_model():
    token = Token(access_token="abxxymdjueuQpd")
    assert token.token_type == "bearer"
