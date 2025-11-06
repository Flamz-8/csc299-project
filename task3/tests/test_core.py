import pytest
from task3.pkms import PKMS

@pytest.fixture
def pkms():
    return PKMS()

def test_task_creation(pkms):
    task_id = pkms.add_task(
        "Test Task",
        "Description",
        priority="High",
        tags=["test"],
        category="Testing"
    )
    task = pkms.tasks[task_id]
    assert task.title == "Test Task"
    assert task.priority == "High"
    assert not task.completed

def test_note_creation(pkms):
    note_id = pkms.add_note(
        "Test Note",
        "Content",
        tags=["test"]
    )
    note = pkms.notes[note_id]
    assert note.title == "Test Note"
    assert "test" in note.tags
