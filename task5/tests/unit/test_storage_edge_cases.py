"""Additional storage tests for edge cases."""

import tempfile
from pathlib import Path

from tasks_cli.storage.task_storage import TaskStorage


def test_long_description_error() -> None:
    """Test that long descriptions raise error."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")
        long_desc = "x" * 1001

        try:
            storage.add_task(long_desc)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "too long" in str(e)


def test_whitespace_only_description() -> None:
    """Test that whitespace-only descriptions raise error."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")

        try:
            storage.add_task("   ")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "cannot be empty" in str(e)


def test_task_timestamp_format() -> None:
    """Test that timestamps are in correct ISO 8601 format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir) / "test.json")
        task = storage.add_task("Test task")

        assert task.timestamp.endswith("Z")
        assert "T" in task.timestamp
        assert len(task.timestamp) == 20  # YYYY-MM-DDTHH:MM:SSZ
