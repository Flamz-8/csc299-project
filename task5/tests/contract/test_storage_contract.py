"""Contract tests for TaskStorage interface."""

import tempfile
from pathlib import Path

import pytest

from tasks_cli.storage.task_storage import TaskStorage


def test_add_task_contract() -> None:
    """Test TaskStorage.add_task contract."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")

        # Add a task
        task = storage.add_task("Test task")

        # Verify contract
        assert task.id == 1
        assert task.description == "Test task"
        assert task.status == "pending"
        assert task.timestamp.endswith("Z")  # ISO 8601 UTC


def test_get_all_tasks_contract() -> None:
    """Test TaskStorage.get_all_tasks contract."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")

        # Empty storage
        tasks = storage.get_all_tasks()
        assert tasks == []

        # Add tasks
        storage.add_task("Task 1")
        storage.add_task("Task 2")

        # Retrieve all tasks
        tasks = storage.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].description == "Task 1"
        assert tasks[1].description == "Task 2"


def test_empty_description_raises_error() -> None:
    """Test that empty description raises ValueError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")

        with pytest.raises(ValueError, match="Task description cannot be empty"):
            storage.add_task("")


def test_sequential_ids() -> None:
    """Test that IDs are sequential."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")

        task1 = storage.add_task("First")
        task2 = storage.add_task("Second")
        task3 = storage.add_task("Third")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
