from tasks3.task_manager import Task, TaskManager

def test_task_creation_and_retrieval():
    manager = TaskManager()
    task_id = manager.add_task("Test Task", "Description", "High")
    task = manager.get_task(task_id)
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.priority == "High"
    assert not task.completed

def test_task_completion_status():
    manager = TaskManager()
    task_id = manager.add_task("Complete Me", "Test task completion", "Medium")
    manager.mark_task_complete(task_id)
    task = manager.get_task(task_id)
    assert task.completed == True
