import os
import json
import pytest
from task3.task_manager import TaskManager

@pytest.fixture
def temp_task_manager(tmp_path):
    original_data_dir = os.path.expanduser("~/.task3")
    TaskManager.data_dir = str(tmp_path)
    manager = TaskManager()
    yield manager
    TaskManager.data_dir = original_data_dir

def test_save_and_load(temp_task_manager):
    # Create a task
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

def test_json_format(temp_task_manager):
    temp_task_manager.add_task("JSON Test", "Testing JSON format")
    
    with open(os.path.join(temp_task_manager.data_dir, "tasks.json")) as f:
        data = json.load(f)
    
    assert "tasks" in data
    assert "next_id" in data
    assert len(data["tasks"]) == 1
