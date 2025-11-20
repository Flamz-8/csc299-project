"""Unit tests for list command."""

from unittest.mock import patch

from tasks_cli.commands.list import list_command
from tasks_cli.models.task import Task


def test_list_command_success() -> None:
    """Test successful task listing."""
    with patch("tasks_cli.commands.list.TaskStorage") as mock_storage_class:
        mock_storage = mock_storage_class.return_value
        mock_storage.get_all_tasks.return_value = [
            Task(1, "Zebra", "2025-11-19T10:30:00Z", "pending"),
            Task(2, "Apple", "2025-11-19T10:31:00Z", "pending"),
            Task(3, "banana", "2025-11-19T10:32:00Z", "pending"),
        ]

        result = list_command()

        assert result == 0
        mock_storage.get_all_tasks.assert_called_once()


def test_list_command_empty() -> None:
    """Test listing with no tasks."""
    with patch("tasks_cli.commands.list.TaskStorage") as mock_storage_class:
        mock_storage = mock_storage_class.return_value
        mock_storage.get_all_tasks.return_value = []

        result = list_command()

        assert result == 0


def test_list_command_error() -> None:
    """Test list command with error."""
    with patch("tasks_cli.commands.list.TaskStorage") as mock_storage_class:
        mock_storage = mock_storage_class.return_value
        mock_storage.get_all_tasks.side_effect = OSError("Cannot read file")

        result = list_command()

        assert result == 1
