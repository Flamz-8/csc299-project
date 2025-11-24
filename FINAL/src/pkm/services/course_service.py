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
