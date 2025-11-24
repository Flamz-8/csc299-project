"""Task service for task management business logic."""

import re
from datetime import date, datetime, timedelta
from pathlib import Path

from pkm.models.common import reset_id_counter
from pkm.models.task import Subtask, Task
from pkm.services.id_generator import generate_task_id
from pkm.storage.json_store import JSONStore
from pkm.storage.schema import deserialize_task, serialize_task


class TaskService:
    """Service for managing tasks."""

    def __init__(self, data_dir: Path) -> None:
        """Initialize task service.

        Args:
            data_dir: Directory containing data.json
        """
        self.store = JSONStore(data_dir / "data.json")
        self._initialize_id_counter()

    def _initialize_id_counter(self) -> None:
        """Initialize the ID counter based on existing tasks."""
        data = self.store.load()
        max_id = 0

        for task_data in data.get("tasks", []):
            task_id = task_data.get("id", "")
            # Extract number from ID (e.g., "t5" -> 5)
            match = re.match(r"t(\d+)", task_id)
            if match:
                num = int(match.group(1))
                max_id = max(max_id, num)

        reset_id_counter("t", max_id)

    def create_task(
        self,
        title: str,
        due_date: datetime | None = None,
        priority: str = "medium",
        course: str | None = None,
    ) -> Task:
        """Create a new task.

        Args:
            title: Task title
            due_date: Optional due date
            priority: Task priority (high, medium, low)
            course: Optional course assignment

        Returns:
            Created task
        """
        task = Task(
            id=generate_task_id(),
            title=title,
            created_at=datetime.now(),
            due_date=due_date,
            priority=priority,  # type: ignore
            completed=False,
            completed_at=None,
            course=course,
            linked_notes=[],
            subtasks=[],
        )

        # Save to storage
        data = self.store.load()
        data["tasks"].append(serialize_task(task))
        self.store.save(data)

        return task

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task if found, None otherwise
        """
        data = self.store.load()
        for task_data in data["tasks"]:
            if task_data["id"] == task_id:
                return deserialize_task(task_data)
        return None

    def list_tasks(self) -> list[Task]:
        """List all tasks.

        Returns:
            List of all tasks
        """
        data = self.store.load()
        return [deserialize_task(task_data) for task_data in data["tasks"]]

    def get_inbox_tasks(self) -> list[Task]:
        """Get all tasks in inbox (course=None).

        Returns:
            List of inbox tasks
        """
        return [task for task in self.list_tasks() if task.course is None]

    def get_tasks_today(self) -> list[Task]:
        """Get all tasks due today.

        Returns:
            List of tasks due today
        """
        today = date.today()
        return [
            task for task in self.list_tasks()
            if task.due_date and task.due_date.date() == today and not task.completed
        ]

    def get_tasks_this_week(self) -> list[Task]:
        """Get all tasks due within 7 days.

        Returns:
            List of tasks due this week
        """
        today = date.today()
        week_end = today + timedelta(days=7)
        return [
            task for task in self.list_tasks()
            if task.due_date
            and today <= task.due_date.date() <= week_end
            and not task.completed
        ]

    def get_tasks_overdue(self) -> list[Task]:
        """Get all overdue tasks (past due and not completed).

        Returns:
            List of overdue tasks
        """
        today = date.today()
        return [
            task for task in self.list_tasks()
            if task.due_date
            and task.due_date.date() < today
            and not task.completed
        ]

    def complete_task(self, task_id: str) -> Task | None:
        """Mark a task as completed.

        Args:
            task_id: Task ID to complete

        Returns:
            Updated task if found, None otherwise
        """
        data = self.store.load()

        for i, task_data in enumerate(data["tasks"]):
            if task_data["id"] == task_id:
                task = deserialize_task(task_data)
                task.completed = True
                task.completed_at = datetime.now()

                # Update in storage
                data["tasks"][i] = serialize_task(task)
                self.store.save(data)

                return task

        return None

    def add_subtask(self, task_id: str, title: str) -> Task | None:
        """Add a subtask to a task.

        Args:
            task_id: Parent task ID
            title: Subtask title

        Returns:
            Updated task if found, None otherwise
        """
        data = self.store.load()

        for i, task_data in enumerate(data["tasks"]):
            if task_data["id"] == task_id:
                task = deserialize_task(task_data)

                # Generate subtask ID (integer)
                subtask_id = len(task.subtasks) + 1

                subtask = Subtask(
                    id=subtask_id,
                    title=title,
                    completed=False,
                )

                task.subtasks.append(subtask)

                # Update in storage
                data["tasks"][i] = serialize_task(task)
                self.store.save(data)

                return task

        return None

    def complete_subtask(self, task_id: str, subtask_id: int) -> Task | None:
        """Mark a subtask as completed.

        Args:
            task_id: Parent task ID
            subtask_id: Subtask ID to complete (integer)

        Returns:
            Updated task if found, None otherwise
        """
        data = self.store.load()

        for i, task_data in enumerate(data["tasks"]):
            if task_data["id"] == task_id:
                task = deserialize_task(task_data)

                for subtask in task.subtasks:
                    if subtask.id == subtask_id:
                        subtask.completed = True

                        # Update in storage
                        data["tasks"][i] = serialize_task(task)
                        self.store.save(data)

                        return task

                return None

        return None

    def organize_task(self, task_id: str, course: str) -> Task | None:
        """Assign a task to a course (move from inbox).

        Args:
            task_id: Task ID to organize
            course: Course name to assign

        Returns:
            Updated task if found, None otherwise
        """
        data = self.store.load()

        for i, task_data in enumerate(data["tasks"]):
            if task_data["id"] == task_id:
                task = deserialize_task(task_data)
                task.course = course

                # Update in storage
                data["tasks"][i] = serialize_task(task)
                self.store.save(data)

                return task

        return None

    def get_tasks_by_course(self, course_name: str) -> list[Task]:
        """Get all tasks for a specific course.

        Args:
            course_name: Course name to filter by

        Returns:
            List of tasks in the course
        """
        return [task for task in self.list_tasks() if task.course == course_name]

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        """Get all tasks with a specific priority.

        Args:
            priority: Priority level (high, medium, low)

        Returns:
            List of tasks with the priority
        """
        return [task for task in self.list_tasks() if task.priority == priority and not task.completed]

    def link_note(self, task_id: str, note_id: str) -> Task | None:
        """Link a note to a task (bidirectional).

        Args:
            task_id: Task ID
            note_id: Note ID to link

        Returns:
            Updated task if found, None otherwise
        """
        data = self.store.load()

        # Update task
        for i, task_data in enumerate(data["tasks"]):
            if task_data["id"] == task_id:
                task = deserialize_task(task_data)

                # Add note to task's linked notes if not already there
                if note_id not in task.linked_notes:
                    task.linked_notes.append(note_id)

                # Update task in storage
                data["tasks"][i] = serialize_task(task)

                # Update note's linked_from_tasks (bidirectional)
                for j, note_data in enumerate(data["notes"]):
                    if note_data["id"] == note_id:
                        if task_id not in note_data.get("linked_from_tasks", []):
                            note_data.setdefault("linked_from_tasks", []).append(task_id)
                        data["notes"][j] = note_data
                        break

                self.store.save(data)
                return task

        return None

    def unlink_note(self, task_id: str, note_id: str) -> Task | None:
        """Unlink a note from a task (bidirectional).

        Args:
            task_id: Task ID
            note_id: Note ID to unlink

        Returns:
            Updated task if found, None otherwise
        """
        data = self.store.load()

        # Update task
        for i, task_data in enumerate(data["tasks"]):
            if task_data["id"] == task_id:
                task = deserialize_task(task_data)

                # Remove note from task's linked notes
                if note_id in task.linked_notes:
                    task.linked_notes.remove(note_id)

                # Update task in storage
                data["tasks"][i] = serialize_task(task)

                # Update note's linked_from_tasks (bidirectional)
                for j, note_data in enumerate(data["notes"]):
                    if note_data["id"] == note_id:
                        linked_tasks = note_data.get("linked_from_tasks", [])
                        if task_id in linked_tasks:
                            linked_tasks.remove(task_id)
                            note_data["linked_from_tasks"] = linked_tasks
                        data["notes"][j] = note_data
                        break

                self.store.save(data)
                return task

        return None
