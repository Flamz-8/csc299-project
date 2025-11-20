"""List command handler."""

import sys

from tasks_cli.storage.task_storage import TaskStorage


def list_command() -> int:
    """List all tasks from storage.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        storage = TaskStorage()
        tasks = storage.get_all_tasks()

        if not tasks:
            print("No tasks found")
            return 0

        # Sort tasks case-insensitively by description
        sorted_tasks = sorted(tasks, key=lambda t: t.description.lower())

        # Display tasks
        for task in sorted_tasks:
            print(f"[{task.id}] {task.description}")

        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
