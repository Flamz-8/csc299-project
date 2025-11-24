"""Course service for managing courses."""

from pathlib import Path

from pkm.models.course import Course
from pkm.services.note_service import NoteService
from pkm.services.task_service import TaskService
from pkm.storage.json_store import JSONStore


class CourseService:
    """Service for managing courses."""

    def __init__(self, data_dir: Path) -> None:
        """Initialize course service.

        Args:
            data_dir: Directory containing data.json
        """
        self.store = JSONStore(data_dir / "data.json")
        self.note_service = NoteService(data_dir)
        self.task_service = TaskService(data_dir)

    def list_courses(self) -> list[Course]:
        """List all courses with note and task counts.

        Returns:
            List of courses with metadata
        """
        data = self.store.load()
        courses: dict[str, Course] = {}

        # Count notes by course
        for note_data in data["notes"]:
            course_name = note_data.get("course")
            if course_name:
                if course_name not in courses:
                    courses[course_name] = Course(name=course_name, note_count=0, task_count=0)
                courses[course_name].note_count += 1

        # Count tasks by course
        for task_data in data["tasks"]:
            course_name = task_data.get("course")
            if course_name:
                if course_name not in courses:
                    courses[course_name] = Course(name=course_name, note_count=0, task_count=0)
                courses[course_name].task_count += 1

        return sorted(courses.values(), key=lambda c: c.name)

    def get_course(self, course_name: str) -> Course | None:
        """Get a course with counts.

        Args:
            course_name: Course name

        Returns:
            Course if exists, None otherwise
        """
        courses = self.list_courses()
        for course in courses:
            if course.name == course_name:
                return course
        return None

    def delete_course(self, course_name: str, reassign_to_inbox: bool = True) -> dict[str, int]:
        """Delete a course and optionally move its items to inbox.

        Args:
            course_name: Course name to delete
            reassign_to_inbox: If True, move items to inbox; if False, delete items

        Returns:
            Dictionary with counts: {"notes": count, "tasks": count}
        """
        data = self.store.load()
        counts = {"notes": 0, "tasks": 0}

        # Handle notes
        for i, note_data in enumerate(data["notes"]):
            if note_data.get("course") == course_name:
                if reassign_to_inbox:
                    note_data["course"] = None
                    data["notes"][i] = note_data
                    counts["notes"] += 1
                else:
                    # Mark for deletion (will remove later)
                    note_data["_to_delete"] = True
                    counts["notes"] += 1

        # Handle tasks
        for i, task_data in enumerate(data["tasks"]):
            if task_data.get("course") == course_name:
                if reassign_to_inbox:
                    task_data["course"] = None
                    data["tasks"][i] = task_data
                    counts["tasks"] += 1
                else:
                    # Mark for deletion
                    task_data["_to_delete"] = True
                    counts["tasks"] += 1

        # Remove items marked for deletion
        if not reassign_to_inbox:
            data["notes"] = [n for n in data["notes"] if not n.get("_to_delete")]
            data["tasks"] = [t for t in data["tasks"] if not t.get("_to_delete")]

        self.store.save(data)
        return counts

