"""Unit tests for add command."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from tasks_cli.commands.add import add_command


def test_add_command_success() -> None:
    """Test successful task addition."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.json"

        with patch("tasks_cli.commands.add.TaskStorage") as mock_storage_class:
            mock_storage = mock_storage_class.return_value
            mock_task = type(
                "Task",
                (),
                {"id": 1, "description": "Test task"},
            )()
            mock_storage.add_task.return_value = mock_task

            result = add_command("Test task")

            assert result == 0
            mock_storage.add_task.assert_called_once_with("Test task")


def test_add_command_empty_description() -> None:
    """Test add command with empty description."""
    with patch("tasks_cli.commands.add.TaskStorage") as mock_storage_class:
        mock_storage = mock_storage_class.return_value
        mock_storage.add_task.side_effect = ValueError(
            "Task description cannot be empty"
        )

        result = add_command("")

        assert result == 1


def test_add_command_io_error() -> None:
    """Test add command with IO error."""
    with patch("tasks_cli.commands.add.TaskStorage") as mock_storage_class:
        mock_storage = mock_storage_class.return_value
        mock_storage.add_task.side_effect = OSError("Cannot write file")

        result = add_command("Test task")

        assert result == 1
