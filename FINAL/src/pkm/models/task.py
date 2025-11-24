"""Task and Subtask model definitions."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class Subtask(BaseModel):
    """A smaller actionable item nested under a parent task.

    Attributes:
        id: Subtask ID (integer, unique within parent task)
        title: Subtask description
        completed: Completion status
    """

    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False

    model_config = {"frozen": False}


class Task(BaseModel):
    """An actionable item with optional deadline, priority, and subtasks.

    Attributes:
        id: Unique identifier (e.g., "t1", "t42")
        title: Task description
        created_at: Timestamp when task was created
        due_date: When task is due (None = no deadline)
        priority: Task priority (high, medium, low)
        completed: Completion status
        completed_at: When task was marked complete
        course: Course assignment (None = inbox)
        linked_notes: Note IDs providing context for this task
        subtasks: Nested subtasks
    """

    id: str = Field(..., pattern=r"^t\d+$")
    title: str = Field(..., min_length=1, max_length=200)
    created_at: datetime
    due_date: datetime | None = None
    priority: Literal["high", "medium", "low"] = "medium"
    completed: bool = False
    completed_at: datetime | None = None
    course: str | None = Field(None, min_length=1, max_length=100)
    linked_notes: list[str] = Field(default_factory=list)
    subtasks: list[Subtask] = Field(default_factory=list)

    @field_validator("completed_at")
    @classmethod
    def validate_completed_at(cls, v: datetime | None, info: dict) -> datetime | None:
        """Ensure completed_at is only set if completed is True."""
        if v is not None and not info.data.get("completed", False):
            raise ValueError("completed_at can only be set if completed is True")
        return v

    @model_validator(mode="after")
    def validate_subtask_ids(self) -> "Task":
        """Ensure subtask IDs are unique and sequential."""
        if self.subtasks:
            ids = [st.id for st in self.subtasks]
            if len(ids) != len(set(ids)):
                raise ValueError("Subtask IDs must be unique")
        return self

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date is None or self.completed:
            return False
        return self.due_date < datetime.now()

    @property
    def is_due_today(self) -> bool:
        """Check if task is due today."""
        if self.due_date is None:
            return False
        return self.due_date.date() == datetime.now().date()

    @property
    def is_due_this_week(self) -> bool:
        """Check if task is due within 7 days."""
        if self.due_date is None:
            return False
        from datetime import timedelta

        return datetime.now() <= self.due_date <= datetime.now() + timedelta(days=7)

    @property
    def subtask_progress(self) -> float:
        """Calculate percentage of completed subtasks."""
        if not self.subtasks:
            return 0.0
        completed = sum(1 for st in self.subtasks if st.completed)
        return (completed / len(self.subtasks)) * 100

    model_config = {"frozen": False}
