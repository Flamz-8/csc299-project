"""Search service for finding notes and tasks."""

from pathlib import Path

from pkm.models.note import Note
from pkm.models.task import Task
from pkm.services.note_service import NoteService
from pkm.services.task_service import TaskService


class SearchService:
    """Service for searching notes and tasks."""

    def __init__(self, data_dir: Path) -> None:
        """Initialize search service.

        Args:
            data_dir: Directory containing data.json
        """
        self.note_service = NoteService(data_dir)
        self.task_service = TaskService(data_dir)

    def search(
        self,
        query: str,
        type_filter: str | None = None,
        course_filter: str | None = None,
        topic_filter: str | None = None,
    ) -> tuple[list[Note], list[Task]]:
        """Search for notes and tasks matching query.

        Args:
            query: Search term (case-insensitive substring match)
            type_filter: Filter by type: "notes", "tasks", or None for both
            course_filter: Filter by course name
            topic_filter: Filter by topic name

        Returns:
            Tuple of (matching_notes, matching_tasks)
        """
        query_lower = query.lower()
        matching_notes: list[Note] = []
        matching_tasks: list[Task] = []

        # Search notes
        if type_filter is None or type_filter == "notes":
            all_notes = self.note_service.list_notes()

            for note in all_notes:
                # Apply filters
                if course_filter and note.course != course_filter:
                    continue
                if topic_filter and topic_filter not in note.topics:
                    continue

                # Search in content, topics, course
                if (query_lower in note.content.lower() or
                    any(query_lower in topic.lower() for topic in note.topics) or
                    (note.course and query_lower in note.course.lower())):
                    matching_notes.append(note)

        # Search tasks
        if type_filter is None or type_filter == "tasks":
            all_tasks = self.task_service.list_tasks()

            for task in all_tasks:
                # Apply filters
                if course_filter and task.course != course_filter:
                    continue

                # Search in title, course
                if (query_lower in task.title.lower() or
                    (task.course and query_lower in task.course.lower())):
                    matching_tasks.append(task)

        return matching_notes, matching_tasks
