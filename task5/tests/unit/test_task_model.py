"""Unit tests for Task model."""

import pytest

from tasks_cli.models.task import Task


def test_task_creation() -> None:
    """Test creating a valid task."""
    task = Task(
        id=1,
        description="Test task",
        timestamp="2025-11-19T10:30:00Z",
        status="pending",
    )
    assert task.id == 1
    assert task.description == "Test task"
    assert task.timestamp == "2025-11-19T10:30:00Z"
    assert task.status == "pending"


def test_task_invalid_id() -> None:
    """Test task with invalid ID raises error."""
    with pytest.raises(ValueError, match="Task ID must be positive"):
        Task(
            id=0,
            description="Test",
            timestamp="2025-11-19T10:30:00Z",
        )


def test_task_empty_description() -> None:
    """Test task with empty description raises error."""
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        Task(
            id=1,
            description="",
            timestamp="2025-11-19T10:30:00Z",
        )


def test_task_long_description() -> None:
    """Test task with too long description raises error."""
    long_desc = "x" * 1001
    with pytest.raises(ValueError, match="Task description too long"):
        Task(
            id=1,
            description=long_desc,
            timestamp="2025-11-19T10:30:00Z",
        )


def test_task_to_dict() -> None:
    """Test task serialization to dictionary."""
    task = Task(
        id=1,
        description="Test task",
        timestamp="2025-11-19T10:30:00Z",
        status="pending",
    )
    result = task.to_dict()
    assert result == {
        "id": 1,
        "description": "Test task",
        "timestamp": "2025-11-19T10:30:00Z",
        "status": "pending",
    }


def test_task_from_dict() -> None:
    """Test task deserialization from dictionary."""
    data = {
        "id": 1,
        "description": "Test task",
        "timestamp": "2025-11-19T10:30:00Z",
        "status": "pending",
    }
    task = Task.from_dict(data)
    assert task.id == 1
    assert task.description == "Test task"
    assert task.timestamp == "2025-11-19T10:30:00Z"
    assert task.status == "pending"
