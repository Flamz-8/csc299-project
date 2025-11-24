"""Unit tests for service layer methods."""

from pathlib import Path

import pytest

from pkm.services.course_service import CourseService
from pkm.services.note_service import NoteService
from pkm.services.task_service import TaskService


class TestNoteService:
    """Unit tests for NoteService methods."""

    def test_delete_note_removes_from_storage(self, temp_data_dir: Path) -> None:
        """Test that delete_note removes note from storage."""
        service = NoteService(temp_data_dir)
        
        # Create a note
        note = service.create_note("Test content")
        note_id = note.id
        
        # Verify note exists
        assert service.get_note(note_id) is not None
        
        # Delete the note
        result = service.delete_note(note_id)
        
        # Verify deletion
        assert result is True
        assert service.get_note(note_id) is None
        
    def test_delete_note_not_found(self, temp_data_dir: Path) -> None:
        """Test deleting a non-existent note returns False."""
        service = NoteService(temp_data_dir)
        
        result = service.delete_note("n999")
        
        assert result is False
        
    def test_delete_note_with_linked_tasks(self, temp_data_dir: Path) -> None:
        """Test deleting a note that's linked to tasks."""
        note_service = NoteService(temp_data_dir)
        task_service = TaskService(temp_data_dir)
        
        # Create note and task
        note = note_service.create_note("Important reference")
        task = task_service.create_task("Task referencing note")
        
        # Link them
        task_service.link_note(task.id, note.id)
        
        # Verify link exists
        updated_note = note_service.get_note(note.id)
        assert task.id in updated_note.linked_from_tasks
        
        # Delete the note
        result = note_service.delete_note(note.id)
        
        # Verify deletion succeeded
        assert result is True
        assert note_service.get_note(note.id) is None


class TestTaskService:
    """Unit tests for TaskService methods."""

    def test_delete_task_removes_from_storage(self, temp_data_dir: Path) -> None:
        """Test that delete_task removes task from storage."""
        service = TaskService(temp_data_dir)
        
        # Create a task
        task = service.create_task("Test task")
        task_id = task.id
        
        # Verify task exists
        assert service.get_task(task_id) is not None
        
        # Delete the task
        result = service.delete_task(task_id)
        
        # Verify deletion
        assert result is True
        assert service.get_task(task_id) is None
        
    def test_delete_task_not_found(self, temp_data_dir: Path) -> None:
        """Test deleting a non-existent task returns False."""
        service = TaskService(temp_data_dir)
        
        result = service.delete_task("t999")
        
        assert result is False
        
    def test_delete_task_cleans_up_note_references(self, temp_data_dir: Path) -> None:
        """Test that deleting a task removes it from linked notes."""
        note_service = NoteService(temp_data_dir)
        task_service = TaskService(temp_data_dir)
        
        # Create note and task
        note = note_service.create_note("Research data")
        task = task_service.create_task("Write report")
        
        # Link them
        task_service.link_note(task.id, note.id)
        
        # Verify link exists
        updated_note = note_service.get_note(note.id)
        assert task.id in updated_note.linked_from_tasks
        updated_task = task_service.get_task(task.id)
        assert note.id in updated_task.linked_notes
        
        # Delete the task
        result = task_service.delete_task(task.id)
        
        # Verify deletion and cleanup
        assert result is True
        assert task_service.get_task(task.id) is None
        
        # Verify note still exists but task reference is removed
        remaining_note = note_service.get_note(note.id)
        assert remaining_note is not None
        assert task.id not in remaining_note.linked_from_tasks
        
    def test_delete_task_with_multiple_linked_notes(self, temp_data_dir: Path) -> None:
        """Test deleting a task cleans up all linked note references."""
        note_service = NoteService(temp_data_dir)
        task_service = TaskService(temp_data_dir)
        
        # Create multiple notes and one task
        note1 = note_service.create_note("Reference 1")
        note2 = note_service.create_note("Reference 2")
        note3 = note_service.create_note("Reference 3")
        task = task_service.create_task("Complex task")
        
        # Link all notes to the task
        task_service.link_note(task.id, note1.id)
        task_service.link_note(task.id, note2.id)
        task_service.link_note(task.id, note3.id)
        
        # Verify all links exist
        for note_id in [note1.id, note2.id, note3.id]:
            note = note_service.get_note(note_id)
            assert task.id in note.linked_from_tasks
        
        # Delete the task
        result = task_service.delete_task(task.id)
        
        # Verify all note references are cleaned up
        assert result is True
        for note_id in [note1.id, note2.id, note3.id]:
            note = note_service.get_note(note_id)
            assert note is not None
            assert task.id not in note.linked_from_tasks
            
    def test_delete_task_with_subtasks(self, temp_data_dir: Path) -> None:
        """Test that deleting a task with subtasks removes everything."""
        service = TaskService(temp_data_dir)
        
        # Create task with subtasks
        task = service.create_task("Parent task")
        service.add_subtask(task.id, "Subtask 1")
        service.add_subtask(task.id, "Subtask 2")
        service.add_subtask(task.id, "Subtask 3")
        
        # Verify subtasks exist
        updated_task = service.get_task(task.id)
        assert len(updated_task.subtasks) == 3
        
        # Delete the task
        result = service.delete_task(task.id)
        
        # Verify deletion
        assert result is True
        assert service.get_task(task.id) is None


class TestCourseService:
    """Unit tests for CourseService methods."""

    def test_delete_course_moves_items_to_inbox(self, temp_data_dir: Path) -> None:
        """Test that delete_course moves items to inbox by default."""
        note_service = NoteService(temp_data_dir)
        task_service = TaskService(temp_data_dir)
        course_service = CourseService(temp_data_dir)
        
        # Create items in a course
        note = note_service.create_note("Course note", course="TestCourse")
        task = task_service.create_task("Course task", course="TestCourse")
        
        # Delete course
        counts = course_service.delete_course("TestCourse", reassign_to_inbox=True)
        
        # Verify counts
        assert counts["notes"] == 1
        assert counts["tasks"] == 1
        
        # Verify items moved to inbox
        updated_note = note_service.get_note(note.id)
        assert updated_note.course is None
        updated_task = task_service.get_task(task.id)
        assert updated_task.course is None
        
    def test_delete_course_deletes_items(self, temp_data_dir: Path) -> None:
        """Test that delete_course can delete all items."""
        note_service = NoteService(temp_data_dir)
        task_service = TaskService(temp_data_dir)
        course_service = CourseService(temp_data_dir)
        
        # Create items in a course
        note = note_service.create_note("Delete me", course="OldCourse")
        task = task_service.create_task("Delete me too", course="OldCourse")
        
        # Delete course and items
        counts = course_service.delete_course("OldCourse", reassign_to_inbox=False)
        
        # Verify counts
        assert counts["notes"] == 1
        assert counts["tasks"] == 1
        
        # Verify items are deleted
        assert note_service.get_note(note.id) is None
        assert task_service.get_task(task.id) is None
        
    def test_delete_course_with_multiple_items(self, temp_data_dir: Path) -> None:
        """Test deleting a course with multiple notes and tasks."""
        note_service = NoteService(temp_data_dir)
        task_service = TaskService(temp_data_dir)
        course_service = CourseService(temp_data_dir)
        
        # Create multiple items
        note1 = note_service.create_note("Note 1", course="BigCourse")
        note2 = note_service.create_note("Note 2", course="BigCourse")
        note3 = note_service.create_note("Note 3", course="BigCourse")
        task1 = task_service.create_task("Task 1", course="BigCourse")
        task2 = task_service.create_task("Task 2", course="BigCourse")
        
        # Delete course
        counts = course_service.delete_course("BigCourse", reassign_to_inbox=True)
        
        # Verify counts
        assert counts["notes"] == 3
        assert counts["tasks"] == 2
        
        # Verify all moved to inbox
        for note_id in [note1.id, note2.id, note3.id]:
            note = note_service.get_note(note_id)
            assert note.course is None
        for task_id in [task1.id, task2.id]:
            task = task_service.get_task(task_id)
            assert task.course is None
            
    def test_delete_course_preserves_other_courses(self, temp_data_dir: Path) -> None:
        """Test that deleting one course doesn't affect others."""
        note_service = NoteService(temp_data_dir)
        task_service = TaskService(temp_data_dir)
        course_service = CourseService(temp_data_dir)
        
        # Create items in two courses
        note1 = note_service.create_note("Keep course note", course="KeepCourse")
        note2 = note_service.create_note("Delete course note", course="DeleteCourse")
        task1 = task_service.create_task("Keep course task", course="KeepCourse")
        task2 = task_service.create_task("Delete course task", course="DeleteCourse")
        
        # Delete one course
        counts = course_service.delete_course("DeleteCourse", reassign_to_inbox=True)
        
        # Verify only DeleteCourse items affected
        assert counts["notes"] == 1
        assert counts["tasks"] == 1
        
        # Verify KeepCourse items unchanged
        updated_note1 = note_service.get_note(note1.id)
        assert updated_note1.course == "KeepCourse"
        updated_task1 = task_service.get_task(task1.id)
        assert updated_task1.course == "KeepCourse"
        
        # Verify DeleteCourse items moved
        updated_note2 = note_service.get_note(note2.id)
        assert updated_note2.course is None
        updated_task2 = task_service.get_task(task2.id)
        assert updated_task2.course is None

