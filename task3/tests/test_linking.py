import pytest
from task3.pkms import PKMS

@pytest.fixture
def pkms_with_items():
    pkms = PKMS()
    task_id = pkms.add_task("Research", "Research topic")
    note_id = pkms.add_note("Research Notes", "Important findings")
    return pkms, task_id, note_id

def test_linking(pkms_with_items):
    pkms, task_id, note_id = pkms_with_items
    assert pkms.link_task_note(task_id, note_id)
    assert note_id in pkms.tasks[task_id].related_notes
    assert task_id in pkms.notes[note_id].related_tasks

def test_invalid_linking(pkms_with_items):
    pkms, task_id, _ = pkms_with_items
    assert not pkms.link_task_note(task_id, 999)  # Non-existent note
