"""
Task3 - Personal Knowledge and Task Management System

This package provides two main components:
1. TaskManager - For managing tasks and todos with JSON persistence
2. KnowledgeBase - For storing and retrieving notes in JSON format

Data Storage:
    All data is stored in JSON format in ~/.task3/:
    - tasks.json: Contains all tasks and their metadata
    - notes.json: Contains all notes and their tags

Quick Start:
    from task3.task_manager import TaskManager
    from task3.knowledge_base import KnowledgeBase

    # Create and manage tasks
    tm = TaskManager()
    task_id = tm.add_task("Learn Python", "Study pytest", "High")
    
    # Create and search notes
    kb = KnowledgeBase()
    kb.add_note("Python Notes", "Testing with pytest", ["python"])

Installation:
    cd task3
    uv install .

Run Tests:
    cd task3
    uv pip install pytest
    uv run pytest
"""

def inc(n: int) -> int:
    return n + 1

def main() -> None:
    """Run example usage of the package"""
    from task3.task_manager import TaskManager
    
    manager = TaskManager()
    task_id = manager.add_task("Example Task", "Testing the system")
    print(f"Created task with ID: {task_id}")

if __name__ == "__main__":
    main()
