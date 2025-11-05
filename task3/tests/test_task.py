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
