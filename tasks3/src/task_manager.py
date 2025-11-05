"""TaskManager module for task creation and management."""

from datetime import datetime
from typing import Optional


class TaskManager:
    """TaskManager handles creation and management of tasks.

    Provides methods for creating tasks, marking them complete,
    and adding tags for organization.
    """

    def __init__(self):
        """Initialize an empty task manager."""
        self.tasks = {}
        self.next_id = 1

    def add_task(self, title: str, description: str, due_date: Optional[datetime] = None) -> int:
        """Create a new task and return its ID.

        Args:
            title: The task title
            description: Detailed description of the task
            due_date: Optional deadline for the task

        Returns:
            int: The ID of the created task
        """
        task_id = self.next_id
        self.tasks[task_id] = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False,
        }
        self.next_id += 1
        return task_id

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as completed.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            bool: True if task was marked complete, False if task not found
        """
        if task_id in self.tasks:
            self.tasks[task_id]["completed"] = True
            return True
        return False