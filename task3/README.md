# Tasks3 - Personal Knowledge and Task Management System

A simple Python package for managing tasks and personal knowledge.

## Installation

```bash
uv install .
```

## Usage

### Task Management
```python
from tasks3.task_manager import TaskManager

# Initialize task manager
task_mgr = TaskManager()

# Add a new task
task_id = task_mgr.add_task(
    title="Learn Python",
    description="Study pytest framework",
    due_date=None  # optional
)

# Mark task as complete
task_mgr.mark_complete(task_id)

# Add tags to task
task_mgr.add_tag(task_id, "python")
```

### Knowledge Base
```python
from tasks3.knowledge_base import KnowledgeBase

# Initialize knowledge base
kb = KnowledgeBase()

# Add a new note
note_id = kb.add_note(
    title="Python Testing",
    content="Pytest is a powerful testing framework",
    tags=["python", "testing"]
)

# Search notes
results = kb.search("pytest")
```
