# Task3 - Personal Knowledge and Task Management System

A simple Python package for managing tasks and personal knowledge.

## Key Features

- **Task Management**
  - Create and track tasks with titles and descriptions
  - Set priority levels (High/Medium/Low)
  - Mark tasks as complete
  - Simple and intuitive API
  - Persistent JSON storage
  - Automatic data saving

- **Knowledge Base**
  - Store and organize notes
  - Tag-based organization
  - Full-text search capability
  - Easy retrieval and management
  - JSON-based storage for easy backup
  - Human-readable data format

## Storage

All data is stored in JSON format in the user's data directory:
- Tasks: `~/.task3/tasks.json`
- Notes: `~/.task3/notes.json`

This makes it easy to:
- Back up your data
- Version control your tasks and notes
- Share data between different machines
- Manually edit if needed (though not recommended)

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

## Testing

### Running All Tests
```bash
cd task3
uv run pytest
```

### Running Specific Test Files
```bash
# Run core functionality tests
uv run pytest tests/test_core.py

# Run search functionality tests
uv run pytest tests/test_search.py

# Run persistence tests
uv run pytest tests/test_persistence.py

# Run linking tests
uv run pytest tests/test_linking.py
```

### Running Individual Tests
```bash
# Run a specific test function
uv run pytest tests/test_search.py::test_search_by_title

# Run tests with specific names (pattern matching)
uv run pytest -k "search"  # Runs all tests with "search" in the name

# Run tests with detailed output
uv run pytest -v
```

### Test Coverage
```bash
# Run tests with coverage report
uv run pytest --cov=task3
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
