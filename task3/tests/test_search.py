import pytest
import os
from task3.pkms import PKMS

@pytest.fixture
def populated_pkms(tmp_path):
    """Create a fresh PKMS instance with test data in a temporary directory"""
    original_dir = os.path.expanduser("~/.task3")
    PKMS.data_dir = str(tmp_path)
    pkms = PKMS()
    pkms.reset()  # Start with clean state
    
    # Add test data
    pkms.add_task("Python Task", "Learn Python", tags=["python"])
    pkms.add_task("Java Task", "Learn Java", tags=["java"])
    pkms.add_note("Python Note", "Python tips", tags=["python"])
    
    yield pkms
    
    # Cleanup
    PKMS.data_dir = original_dir

def test_search_by_title(populated_pkms):
    tasks, notes = populated_pkms.search("python")
    assert len(tasks) == 1
    assert tasks[0].title == "Python Task"

def test_search_by_tags(populated_pkms):
    tasks, notes = populated_pkms.search("java")
    assert len(tasks) == 1
    assert tasks[0].title == "Java Task"
