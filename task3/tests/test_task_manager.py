import pytest
from datetime import datetime
from task3.task_manager import TaskManager

def test_task_creation():
    manager = TaskManager()
    task_id = manager.add_task("Test Task", "Description")
    task = manager.get_task(task_id)
    
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert isinstance(task.created_date, datetime)
    assert not task.completed

def test_task_completion():
    manager = TaskManager()
    task_id = manager.add_task("Complete Me", "Test completion")
    
    assert manager.mark_complete(task_id)
    task = manager.get_task(task_id)
    assert task.completed
