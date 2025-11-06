import pytest
from task3.pkms import PKMS

@pytest.fixture
def populated_pkms():
    pkms = PKMS()
    pkms.add_task("Python Task", "Learn Python", tags=["python"])
    pkms.add_task("Java Task", "Learn Java", tags=["java"])
    pkms.add_note("Python Note", "Python tips", tags=["python"])
    return pkms

def test_search_by_title(populated_pkms):
    tasks, notes = populated_pkms.search("python")
    assert len(tasks) == 1
    assert len(notes) == 1
    assert tasks[0].title == "Python Task"

def test_search_by_tags(populated_pkms):
    tasks, notes = populated_pkms.search("java")
    assert len(tasks) == 1
    assert len(notes) == 0
    assert tasks[0].title == "Java Task"
