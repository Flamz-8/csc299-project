import pytest
import os
from task3.pkms import PKMS

@pytest.fixture
def populated_pkms(tmp_path):
    """Create a fresh PKMS instance with test data"""
    original_dir = os.path.expanduser("~/.task3")
    PKMS.data_dir = str(tmp_path)
    system = PKMS()
    
    # Add test data
    system.add_task("Python Task", "Learn Python", tags=["python"])
    system.add_task("Java Task", "Learn Java", tags=["java"])
    system.add_note("Python Note", "Python tips", tags=["python"])
    
    yield system
    PKMS.data_dir = original_dir

def test_search_by_title(populated_pkms):
    tasks, notes = populated_pkms.search("python")
    assert len(tasks) == 1
    assert tasks[0].title == "Python Task"

def test_search_by_tags(populated_pkms):
    tasks, notes = populated_pkms.search("java")
    assert len(tasks) == 1
    assert tasks[0].title == "Java Task"
