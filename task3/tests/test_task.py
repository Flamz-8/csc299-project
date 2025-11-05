from tasks3.task_manager import Task, TaskManager

def test_task_creation():
    """Test basic task creation with properties"""
    task = Task("Learn pytest", "Study testing in Python", priority=1)
    assert task.title == "Learn pytest"
    assert task.description == "Study testing in Python"
    assert task.priority == 1
    assert not task.completed

def test_task_completion():
    """Test marking tasks as complete"""
    manager = TaskManager()
    task_id = manager.add_task("Test task", "Description", priority=2)
    manager.complete_task(task_id)
    task = manager.get_task(task_id)
    assert task.completed == True
