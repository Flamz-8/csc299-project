"""Note service for note management business logic."""

import re
from datetime import datetime
from pathlib import Path

from pkm.models.common import reset_id_counter
from pkm.models.note import Note
from pkm.services.id_generator import generate_note_id
from pkm.storage.json_store import JSONStore
from pkm.storage.schema import deserialize_note, serialize_note


class NoteService:
    """Service for managing notes."""

    def __init__(self, data_dir: Path) -> None:
        """Initialize note service.

        Args:
            data_dir: Directory containing data.json
        """
        self.store = JSONStore(data_dir / "data.json")
        self._initialize_id_counter()

    def _initialize_id_counter(self) -> None:
        """Initialize the ID counter based on existing notes."""
        data = self.store.load()
        max_id = 0

        for note_data in data.get("notes", []):
            note_id = note_data.get("id", "")
            # Extract number from ID (e.g., "n5" -> 5)
            match = re.match(r"n(\d+)", note_id)
            if match:
                num = int(match.group(1))
                max_id = max(max_id, num)

        reset_id_counter("n", max_id)

    def create_note(
        self, content: str, course: str | None = None, topics: list[str] | None = None
    ) -> Note:
        """Create a new note.

        Args:
            content: Note content
            course: Optional course assignment
            topics: Optional topic tags

        Returns:
            Created note
        """
        now = datetime.now()
        note = Note(
            id=generate_note_id(),
            content=content,
            created_at=now,
            modified_at=now,
            course=course,
            topics=topics or [],
            linked_from_tasks=[],
        )

        # Save to storage
        data = self.store.load()
        data["notes"].append(serialize_note(note))
        self.store.save(data)

        return note

    def get_note(self, note_id: str) -> Note | None:
        """Get a note by ID.

        Args:
            note_id: Note ID

        Returns:
            Note if found, None otherwise
        """
        data = self.store.load()
        for note_data in data["notes"]:
            if note_data["id"] == note_id:
                return deserialize_note(note_data)
        return None

    def list_notes(self) -> list[Note]:
        """List all notes.

        Returns:
            List of all notes
        """
        data = self.store.load()
        return [deserialize_note(note_data) for note_data in data["notes"]]

    def get_inbox_notes(self) -> list[Note]:
        """Get all notes in inbox (course=None).

        Returns:
            List of inbox notes
        """
        return [note for note in self.list_notes() if note.course is None]

    def organize_note(self, note_id: str, course: str) -> Note | None:
        """Assign a note to a course (move from inbox).

        Args:
            note_id: Note ID to organize
            course: Course name to assign

        Returns:
            Updated note if found, None otherwise
        """
        data = self.store.load()

        for i, note_data in enumerate(data["notes"]):
            if note_data["id"] == note_id:
                note = deserialize_note(note_data)
                note.course = course

                # Update in storage
                data["notes"][i] = serialize_note(note)
                self.store.save(data)

                return note

        return None

    def get_notes_by_course(self, course_name: str) -> list[Note]:
        """Get all notes for a specific course.

        Args:
            course_name: Course name to filter by

        Returns:
            List of notes in the course
        """
        return [note for note in self.list_notes() if note.course == course_name]

    def get_notes_by_topic(self, topic_name: str) -> list[Note]:
        """Get all notes with a specific topic.

        Args:
            topic_name: Topic to filter by

        Returns:
            List of notes with the topic
        """
        return [note for note in self.list_notes() if topic_name in note.topics]

    def add_topics(self, note_id: str, topics: list[str]) -> Note | None:
        """Add topics to a note.

        Args:
            note_id: Note ID
            topics: Topics to add

        Returns:
            Updated note if found, None otherwise
        """
        data = self.store.load()

        for i, note_data in enumerate(data["notes"]):
            if note_data["id"] == note_id:
                note = deserialize_note(note_data)

                # Add topics (avoid duplicates)
                for topic in topics:
                    if topic not in note.topics:
                        note.topics.append(topic)

                # Update in storage
                data["notes"][i] = serialize_note(note)
                self.store.save(data)

                return note

        return None

    def update_note(self, note_id: str, new_content: str) -> Note | None:
        """Update a note's content.

        Args:
            note_id: Note ID to update
            new_content: New content for the note

        Returns:
            Updated note if found, None otherwise
        """
        data = self.store.load()

        for i, note_data in enumerate(data["notes"]):
            if note_data["id"] == note_id:
                note = deserialize_note(note_data)
                note.content = new_content
                note.modified_at = datetime.now()

                # Update in storage
                data["notes"][i] = serialize_note(note)
                self.store.save(data)

                return note

        return None

    def remove_topic(self, note_id: str, topic: str) -> Note | None:
        """Remove a topic from a note.

        Args:
            note_id: Note ID
            topic: Topic to remove

        Returns:
            Updated note if found, None otherwise
        """
        data = self.store.load()

        for i, note_data in enumerate(data["notes"]):
            if note_data["id"] == note_id:
                note = deserialize_note(note_data)

                # Remove topic if present
                if topic in note.topics:
                    note.topics.remove(topic)

                # Update in storage
                data["notes"][i] = serialize_note(note)
                self.store.save(data)

                return note

        return None

    def delete_note(self, note_id: str) -> bool:
        """Delete a note.

        Args:
            note_id: Note ID to delete

        Returns:
            True if deleted, False if not found
        """
        data = self.store.load()

        for i, note_data in enumerate(data["notes"]):
            if note_data["id"] == note_id:
                del data["notes"][i]
                self.store.save(data)
                return True

        return False
