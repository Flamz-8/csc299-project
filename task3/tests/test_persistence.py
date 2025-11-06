import os
import json
import pytest
from task3.pkms import PKMS

@pytest.fixture
def temp_pkms(tmp_path):
    """Create a PKMS instance with temporary storage"""
    original_data_dir = os.path.expanduser("~/.task3")
    PKMS.data_dir = str(tmp_path)
    manager = PKMS()
    yield manager
    PKMS.data_dir = original_data_dir

def test_save_and_load(temp_pkms):
    # Create test data
    task_id = temp_pkms.add_task(
        "Test Task",
        "Test Description",
        priority="High",
        tags=["test"]
    )
    
    # Create new instance to test loading
    new_pkms = PKMS()
    loaded_task = new_pkms.tasks.get(task_id)
    
    assert loaded_task is not None
    assert loaded_task.title == "Test Task"
    assert loaded_task.priority == "High"
    assert "test" in loaded_task.tags

def test_json_file_structure(temp_pkms):
    # Add test data
    temp_pkms.add_task("JSON Test", "Testing JSON")
    
    # Verify JSON file exists and has correct structure
    tasks_file = os.path.join(temp_pkms.data_dir, "tasks.json")
    assert os.path.exists(tasks_file)
    
    with open(tasks_file) as f:
        data = json.load(f)
        assert "tasks" in data
        assert "next_id" in data
        assert isinstance(data["tasks"], list)
