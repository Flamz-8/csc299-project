import os
import json
import pytest
from task3.task_manager import TaskManager
from task3.pkms import PKMS

@pytest.fixture
def temp_task_manager(tmp_path):
    original_data_dir = os.path.expanduser("~/.task3")
    TaskManager.data_dir = str(tmp_path)
    manager = TaskManager()
    yield manager
    TaskManager.data_dir = original_data_dir

@pytest.fixture
def temp_pkms(tmp_path):
    PKMS.data_dir = str(tmp_path)
    return PKMS()

def test_save_and_load(temp_task_manager, temp_pkms):
    # TaskManager test
    task_id = temp_task_manager.add_task(
        "Test Task",
        "Test Description",
        tags=["test"],
        category="Testing"
    )
    
    # Create new manager instance to load from file
    new_manager = TaskManager()
    loaded_task = new_manager.get_task(task_id)
    
    assert loaded_task is not None
    assert loaded_task.title == "Test Task"
    assert "test" in loaded_task.tags

    # PKMS test
    task_id = temp_pkms.add_task("Save Test", "Testing save")
    note_id = temp_pkms.add_note("Load Test", "Testing load")
    
    # Create new instance to test loading
    new_pkms = PKMS()
    assert task_id in new_pkms.tasks
    assert note_id in new_pkms.notes

def test_json_format(temp_task_manager):
    temp_task_manager.add_task("JSON Test", "Testing JSON format")
    
    with open(os.path.join(temp_task_manager.data_dir, "tasks.json")) as f:
        data = json.load(f)
    
    assert "tasks" in data
    assert "next_id" in data
    assert len(data["tasks"]) == 1

def test_persistence_after_linking(temp_pkms):
    task_id = temp_pkms.add_task("Link Test", "Testing")
    note_id = temp_pkms.add_note("Link Note", "Testing")
    temp_pkms.link_task_note(task_id, note_id)
    
    # Verify links persist after reload
    new_pkms = PKMS()
    assert note_id in new_pkms.tasks[task_id].related_notes
