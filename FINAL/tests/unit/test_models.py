"""Unit tests for Pydantic models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from pkm.models.common import generate_id
from pkm.models.course import Course
from pkm.models.note import Note
from pkm.models.task import Subtask, Task


class TestIDGeneration:
    """Tests for ID generation."""

    def test_generate_note_id(self) -> None:
        """Test generating a note ID."""
        note_id = generate_id("n")
        assert note_id.startswith("n")
        # Format: n{number} (e.g., n1, n42)
        assert note_id[1:].isdigit()
        assert len(note_id) >= 2  # At least "n1"

    def test_generate_task_id(self) -> None:
        """Test generating a task ID."""
        task_id = generate_id("t")
        assert task_id.startswith("t")
        assert task_id[1:].isdigit()
        assert len(task_id) >= 2  # At least "t1"

    def test_ids_are_unique(self) -> None:
        """Test that generated IDs are unique."""
        ids = [generate_id("n") for _ in range(100)]
        assert len(ids) == len(set(ids))


class TestNoteModel:
    """Tests for Note model."""

    def test_create_valid_note(self) -> None:
        """Test creating a valid note."""
        note = Note(
            id="n1",
            content="Test note content",
            created_at=datetime(2025, 11, 23, 10, 30, 45),
            modified_at=datetime(2025, 11, 23, 10, 30, 45),
        )
        assert note.id == "n1"
        assert note.content == "Test note content"
        assert note.course is None
        assert note.topics == []
        assert note.linked_from_tasks == []

    def test_note_with_course_and_topics(self) -> None:
        """Test note with course and topics."""
        note = Note(
            id="n2",
            content="Photosynthesis notes",
            created_at=datetime.now(),
            modified_at=datetime.now(),
            course="Biology 101",
            topics=["Photosynthesis", "Cell Structure"],
        )
        assert note.course == "Biology 101"
        assert len(note.topics) == 2

    def test_note_content_validation(self) -> None:
        """Test that empty content is rejected."""
        with pytest.raises(ValidationError):
            Note(
                id="n3",
                content="",
                created_at=datetime.now(),
                modified_at=datetime.now(),
            )

    def test_note_content_max_length(self) -> None:
        """Test that content over 10,000 chars is rejected."""
        with pytest.raises(ValidationError):
            Note(
                id="n4",
                content="a" * 10001,
                created_at=datetime.now(),
                modified_at=datetime.now(),
            )

    def test_note_id_pattern(self) -> None:
        """Test that invalid ID pattern is rejected."""
        with pytest.raises(ValidationError):
            Note(
                id="invalid_id",
                content="Test",
                created_at=datetime.now(),
                modified_at=datetime.now(),
            )

    def test_note_topic_length_validation(self) -> None:
        """Test that topics over 50 chars are rejected."""
        with pytest.raises(ValidationError):
            Note(
                id="n5",
                content="Test",
                created_at=datetime.now(),
                modified_at=datetime.now(),
                topics=["a" * 51],
            )


class TestTaskModel:
    """Tests for Task model."""

    def test_create_valid_task(self) -> None:
        """Test creating a valid task."""
        task = Task(
            id="t1",
            title="Submit lab report",
            created_at=datetime(2025, 11, 23, 14, 0, 0),
        )
        assert task.id == "t1"
        assert task.title == "Submit lab report"
        assert task.priority == "medium"
        assert not task.completed
        assert task.completed_at is None

    def test_task_with_due_date_and_priority(self) -> None:
        """Test task with due date and priority."""
        task = Task(
            id="t2",
            title="Submit lab report",
            created_at=datetime.now(),
            due_date=datetime(2025, 11, 25, 23, 59, 59),
            priority="high",
        )
        assert task.due_date is not None
        assert task.priority == "high"

    def test_task_with_subtasks(self) -> None:
        """Test task with subtasks."""
        task = Task(
            id="t3",
            title="Complete project",
            created_at=datetime.now(),
            subtasks=[
                Subtask(id=1, title="Research", completed=True),
                Subtask(id=2, title="Write code", completed=False),
            ],
        )
        assert len(task.subtasks) == 2
        assert task.subtasks[0].completed

    def test_task_title_validation(self) -> None:
        """Test that empty title is rejected."""
        with pytest.raises(ValidationError):
            Task(id="t4", title="", created_at=datetime.now())

    def test_task_title_max_length(self) -> None:
        """Test that title over 200 chars is rejected."""
        with pytest.raises(ValidationError):
            Task(
                id="t5", title="a" * 201, created_at=datetime.now()
            )

    def test_task_invalid_priority(self) -> None:
        """Test that invalid priority is rejected."""
        with pytest.raises(ValidationError):
            Task(
                id="t6",
                title="Test",
                created_at=datetime.now(),
                priority="urgent",  # type: ignore
            )

    def test_task_completed_at_validation(self) -> None:
        """Test that completed_at can only be set if completed is True."""
        with pytest.raises(ValidationError):
            Task(
                id="t7",
                title="Test",
                created_at=datetime.now(),
                completed=False,
                completed_at=datetime.now(),
            )

    def test_task_is_overdue(self) -> None:
        """Test is_overdue property."""
        task = Task(
            id="t8",
            title="Test",
            created_at=datetime.now(),
            due_date=datetime(2020, 1, 1),  # Past date
        )
        assert task.is_overdue

    def test_task_not_overdue_if_completed(self) -> None:
        """Test that completed tasks are not overdue."""
        task = Task(
            id="t9",
            title="Test",
            created_at=datetime.now(),
            due_date=datetime(2020, 1, 1),
            completed=True,
            completed_at=datetime.now(),
        )
        assert not task.is_overdue

    def test_task_subtask_progress(self) -> None:
        """Test subtask progress calculation."""
        task = Task(
            id="t10",
            title="Test",
            created_at=datetime.now(),
            subtasks=[
                Subtask(id=1, title="Sub1", completed=True),
                Subtask(id=2, title="Sub2", completed=True),
                Subtask(id=3, title="Sub3", completed=False),
            ],
        )
        assert task.subtask_progress == pytest.approx(66.666, rel=0.01)

    def test_task_subtask_unique_ids(self) -> None:
        """Test that duplicate subtask IDs are rejected."""
        with pytest.raises(ValidationError):
            Task(
                id="t11",
                title="Test",
                created_at=datetime.now(),
                subtasks=[
                    Subtask(id=1, title="Sub1"),
                    Subtask(id=1, title="Sub2"),  # Duplicate ID
                ],
            )


class TestCourseModel:
    """Tests for Course model."""

    def test_create_valid_course(self) -> None:
        """Test creating a valid course."""
        course = Course(name="Biology 101")
        assert course.name == "Biology 101"
        assert course.note_count == 0
        assert course.task_count == 0

    def test_course_with_counts(self) -> None:
        """Test course with note/task counts."""
        course = Course(name="Math 201", note_count=5, task_count=3)
        assert course.note_count == 5
        assert course.task_count == 3

    def test_course_name_validation(self) -> None:
        """Test that empty course name is rejected."""
        with pytest.raises(ValidationError):
            Course(name="")
