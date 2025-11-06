# Task3 - Personal Knowledge and Task Management System

A simple Python package for managing tasks and personal knowledge.

## Installation

1. Clone the repository
2. Navigate to the task3 directory
3. Install using uv:
```bash
uv install .
```

## Usage

### Task Management

```python
from task3.task_manager import TaskManager

# Initialize task manager
manager = TaskManager()

# Create new tasks
task_id = manager.add_task(
    title="Learn Python",
    description="Study pytest",
    priority="High"  # Optional, defaults to "Medium"
)

# Get task details
task = manager.get_task(task_id)
print(f"Task: {task.title}")

# Mark task complete
manager.mark_complete(task_id)
```

### Knowledge Base

```python
from task3.knowledge_base import KnowledgeBase

# Initialize knowledge base
kb = KnowledgeBase()

# Add notes
note_id = kb.add_note(
    title="Python Testing",
    content="Pytest is a testing framework",
    tags=["python", "testing"]
)

# Search notes
results = kb.search("python")
for note in results:
    print(f"Found: {note.title}")
```

## Development

### Running Tests
1. Install pytest:
```bash
uv pip install pytest
```

2. Run tests:
```bash
uv run pytest
```
