"""Unit tests for TaskStorage."""

import json
import tempfile
from pathlib import Path

import pytest

from tasks_cli.storage.task_storage import TaskStorage


def test_read_tasks_missing_file() -> None:
    """Test reading tasks from non-existent file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "missing.json")
        tasks = storage._read_tasks()
        assert tasks == []


def test_write_tasks() -> None:
    """Test writing tasks to file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")
        tasks = [
            storage.add_task("Task 1"),
            storage.add_task("Task 2"),
        ]

        # Verify file exists and contains data
        assert storage.file_path.exists()
        with storage.file_path.open() as f:
            data = json.load(f)
            assert len(data) == 2


def test_corrupted_json() -> None:
    """Test handling of corrupted JSON file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.json"

        # Write corrupted JSON
        test_file.write_text("{ invalid json }")

        storage = TaskStorage(test_file)

        with pytest.raises(ValueError, match="Corrupted JSON"):
            storage._read_tasks()

        # Verify backup was created
        backup_file = test_file.with_suffix(".json.backup")
        assert backup_file.exists()


def test_get_next_id_empty() -> None:
    """Test ID generation with no tasks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")
        assert storage._get_next_id([]) == 1


def test_get_next_id_existing() -> None:
    """Test ID generation with existing tasks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        assert storage._get_next_id([task1, task2]) == 3
