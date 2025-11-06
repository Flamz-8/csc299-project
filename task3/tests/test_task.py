from task3.task_manager import Task, TaskManager

def test_task_creation():
    """Test basic task creation with properties"""
    manager = TaskManager()
    task_id = manager.add_task("Learn pytest", "Study testing in Python")
    task = manager.get_task(task_id)
    assert task.title == "Learn pytest"
    assert task.description == "Study testing in Python"
    assert not task.completed

def test_task_completion():
    """Test marking tasks as complete"""
    manager = TaskManager()
    task_id = manager.add_task("Test task", "Description")
    manager.mark_complete(task_id)
    task = manager.get_task(task_id)
    assert task.completed == True

def test_task_with_tags():
    manager = TaskManager()
    task_id = manager.add_task(
        "Learn PKMS",
        "Study knowledge management",
        tags=["study", "pkms"],
        category="Education"
    )
    task = manager.get_task(task_id)
    assert len(task.tags) == 2
    assert "pkms" in task.tags
    assert task.category == "Education"

def test_task_search():
    manager = TaskManager()
    manager.add_task(
        "Python Study",
        "Learn Python basics",
        tags=["python"],
        category="Programming"
    )
    manager.add_task(
        "Java Study",
        "Learn Java basics",
        tags=["java"],
        category="Programming"
    )
    
    results = manager.search("python")
    assert len(results) == 1
    assert results[0].title == "Python Study"
    
    results = manager.search("programming")
    assert len(results) == 2
