"""Add command handler."""

import sys

from tasks_cli.storage.task_storage import TaskStorage


def add_command(description: str) -> int:
    """Add a new task to storage.

    Args:
        description: Task description text

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        storage = TaskStorage()
        task = storage.add_task(description)
        print(f"Task added: [{task.id}] {task.description}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
