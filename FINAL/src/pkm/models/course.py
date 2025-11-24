"""Course model definition."""

from pydantic import BaseModel, Field


class Course(BaseModel):
    """A course/subject for organizing notes and tasks.

    Attributes:
        name: Course name (e.g., "Biology 101")
        note_count: Number of notes in this course (computed)
        task_count: Number of tasks in this course (computed)
    """

    name: str = Field(..., min_length=1, max_length=100)
    note_count: int = Field(default=0, ge=0)
    task_count: int = Field(default=0, ge=0)

    model_config = {"frozen": False}
