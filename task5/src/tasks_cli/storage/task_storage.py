"""Storage layer for persistent task management."""

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from tasks_cli.models.task import Task


class TaskStorage:
    """Handles persistent storage of tasks in JSON format.

    This class is completely agnostic to how it's called (CLI, API, tests).
    It provides a clean interface for CRUD operations on tasks.
    """

    def __init__(self, file_path: Path | None = None) -> None:
        """Initialize storage with file path.

        Args:
            file_path: Path to JSON storage file. Defaults to ~/.tasks.json
        """
        self.file_path = file_path or Path.home() / ".tasks.json"

    def add_task(self, description: str) -> Task:
        """Add a new task to storage.

        Args:
            description: Task description (1-1000 characters)

        Returns:
            Created Task object with assigned ID and timestamp

        Raises:
            ValueError: If description is empty or too long
            IOError: If file cannot be written
        """
        # Validate description
        if not description or not description.strip():
            msg = "Task description cannot be empty"
            raise ValueError(msg)

        if len(description) > 1000:
            msg = (
                f"Task description too long ({len(description)} chars), "
                f"maximum is 1000 characters"
            )
            raise ValueError(msg)

        # Read existing tasks
        tasks = self._read_tasks()

        # Generate next ID and timestamp
        task_id = self._get_next_id(tasks)
        timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Create new task
        new_task = Task(
            id=task_id,
            description=description.strip(),
            timestamp=timestamp,
            status="pending",
        )

        # Append and write
        tasks.append(new_task)
        self._write_tasks(tasks)

        return new_task

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks from storage.

        Returns:
            List of Task objects, empty list if no tasks exist

        Raises:
            IOError: If file exists but cannot be read
            ValueError: If JSON is corrupted
        """
        return self._read_tasks()

    def _read_tasks(self) -> list[Task]:
        """Read and parse tasks from JSON file.

        Returns:
            List of Task objects
            Empty list if file doesn't exist

        Raises:
            ValueError: If JSON is corrupted (after backup)
        """
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(task_dict) for task_dict in data]
        except json.JSONDecodeError as e:
            # Backup corrupted file
            backup_path = self.file_path.with_suffix(".json.backup")
            self.file_path.rename(backup_path)
            msg = (
                f"Corrupted JSON file detected. Backed up to {backup_path}. "
                f"Starting with empty task list."
            )
            raise ValueError(msg) from e
        except (OSError, PermissionError) as e:
            msg = f"Cannot read tasks file: {e}"
            raise OSError(msg) from e

    def _write_tasks(self, tasks: list[Task]) -> None:
        """Write tasks to JSON file atomically.

        Args:
            tasks: List of tasks to write

        Raises:
            IOError: If write fails
        """
        try:
            # Ensure parent directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temporary file first (atomic write pattern)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.file_path.parent,
                delete=False,
                suffix=".tmp",
            ) as tmp_file:
                task_dicts = [task.to_dict() for task in tasks]
                json.dump(task_dicts, tmp_file, indent=2, ensure_ascii=False)
                tmp_file.flush()
                tmp_path = Path(tmp_file.name)

            # Atomic rename (or as close as possible on Windows)
            tmp_path.replace(self.file_path)

        except (OSError, PermissionError) as e:
            msg = f"Cannot write tasks file: {e}"
            raise OSError(msg) from e

    def _get_next_id(self, tasks: list[Task]) -> int:
        """Calculate next sequential ID.

        Args:
            tasks: List of existing tasks

        Returns:
            Next available ID (max existing ID + 1, or 1 if no tasks)
        """
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1
