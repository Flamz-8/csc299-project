import pytest
import os
from task3.pkms import PKMS

@pytest.fixture
def pkms(tmp_path):
    """Create a fresh PKMS instance with temporary storage for each test"""
    original_dir = os.path.expanduser("~/.task3")
    PKMS.data_dir = str(tmp_path)
    system = PKMS()
    yield system
    PKMS.data_dir = original_dir

def test_task_creation(pkms):
    task_id = pkms.add_task(
        "Test Task",
        "Description",
        priority="High",
        tags=["test"],
        category="Testing"
    )
    task = pkms.tasks.get(task_id)
    assert task.title == "Test Task"
    assert task.priority == "High"
    assert "test" in task.tags

def test_note_creation(pkms):
    note_id = pkms.add_note(
        "Test Note",
        "Test content",
        tags=["test"]
    )
    note = pkms.notes.get(note_id)
    assert note.title == "Test Note"
    assert "test" in note.tags

def test_task_note_linking(pkms):
    task_id = pkms.add_task("Task", "Description")
    note_id = pkms.add_note("Note", "Content")
    
    pkms.link_task_note(task_id, note_id)
    assert note_id in pkms.tasks[task_id].related_notes
    assert task_id in pkms.notes[note_id].related_tasks

def test_search(pkms):
    pkms.add_task("Python Task", "Learn Python", tags=["python"])
    pkms.add_note("Python Note", "Python tips", tags=["python"])
    
    tasks, notes = pkms.search("python")
    assert len(tasks) == 1
    assert len(notes) == 1
    assert tasks[0].title == "Python Task"
    assert notes[0].title == "Python Note"
