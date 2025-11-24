"""JSON storage schema definition."""

from typing import TypedDict

from pkm.models.course import Course
from pkm.models.note import Note
from pkm.models.task import Task


class DataSchema(TypedDict):
    """JSON data storage schema.

    Structure:
        {
            "notes": [...],
            "tasks": [...],
            "courses": [...]
        }
    """

    notes: list[dict]
    tasks: list[dict]
    courses: list[dict]


def create_empty_schema() -> DataSchema:
    """Create an empty data schema."""
    return {"notes": [], "tasks": [], "courses": []}


def serialize_note(note: Note) -> dict:
    """Serialize a Note to JSON-compatible dict."""
    return note.model_dump(mode="json")


def serialize_task(task: Task) -> dict:
    """Serialize a Task to JSON-compatible dict."""
    return task.model_dump(mode="json")


def serialize_course(course: Course) -> dict:
    """Serialize a Course to JSON-compatible dict."""
    return course.model_dump(mode="json")


def deserialize_note(data: dict) -> Note:
    """Deserialize a dict to Note model."""
    return Note.model_validate(data)


def deserialize_task(data: dict) -> Task:
    """Deserialize a dict to Task model."""
    return Task.model_validate(data)


def deserialize_course(data: dict) -> Course:
    """Deserialize a dict to Course model."""
    return Course.model_validate(data)
