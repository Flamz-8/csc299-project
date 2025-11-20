# API Contracts: Task Management CLI

**Feature**: Task Management CLI  
**Date**: 2025-11-19  
**Phase**: Phase 1 - Design

## Overview

This document defines the public API contracts for the task management CLI. These contracts specify the interfaces that must be implemented and the behavior that must be maintained across the application.

## Storage Layer Contract

### TaskStorage Interface

**Module**: `tasks_cli.storage.task_storage`

**Purpose**: Provide an abstract interface for persistent task storage, independent of implementation details.

```python
from pathlib import Path
from typing import List, Optional
from tasks_cli.models.task import Task

class TaskStorage:
    """Abstract interface for task storage operations.
    
    This interface defines the contract that any storage implementation
    must satisfy. The CLI layer depends only on this interface, not on
    implementation details (JSON, database, etc.).
    
    Contract Guarantees:
    - Thread-safe for single-user scenarios
    - Atomic operations (all-or-nothing writes)
    - Automatic file creation if missing
    - Graceful corruption handling
    """
    
    def __init__(self, file_path: Optional[Path] = None):
        """Initialize storage with optional custom file path.
        
        Args:
            file_path: Path to storage file. If None, uses ~/.tasks.json
            
        Postconditions:
            - self.file_path is set to provided path or default
            - No file I/O performed (lazy initialization)
        """
        ...
    
    def add_task(self, description: str) -> Task:
        """Add a new task to storage.
        
        Args:
            description: Task description text
            
        Returns:
            Created Task object with assigned ID and timestamp
            
        Raises:
            ValueError: If description is empty or > 1000 characters
            IOError: If file cannot be written (permissions, disk full)
            
        Preconditions:
            - description must be non-empty after stripping whitespace
            - description length <= 1000 characters
            
        Postconditions:
            - Task is added to storage file
            - Task has unique sequential ID (max(existing) + 1 or 1)
            - Task has ISO 8601 UTC timestamp
            - Task has status "pending"
            - File is written atomically (temp + rename)
            - Returns the created task
            
        Example:
            >>> storage = TaskStorage()
            >>> task = storage.add_task("Buy groceries")
            >>> assert task.id == 1
            >>> assert task.description == "Buy groceries"
            >>> assert task.status == "pending"
        """
        ...
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from storage.
        
        Returns:
            List of Task objects, ordered as stored (not sorted)
            Empty list if no tasks exist or file doesn't exist
            
        Raises:
            IOError: If file exists but cannot be read (permissions)
            
        Preconditions:
            - None (handles missing file gracefully)
            
        Postconditions:
            - Returns all valid tasks from storage
            - Invalid tasks logged as warnings and skipped
            - Corrupted files backed up and empty list returned
            - Does NOT modify storage
            
        Side Effects:
            - If file is corrupted: creates .tasks.json.backup file
            - Logs warnings for invalid tasks
            
        Example:
            >>> storage = TaskStorage()
            >>> tasks = storage.get_all_tasks()
            >>> assert isinstance(tasks, list)
            >>> assert all(isinstance(t, Task) for t in tasks)
        """
        ...
```

### Internal Methods (Implementation-Specific)

These methods are part of the implementation but not the public contract:

```python
class TaskStorage:
    # ... public methods above ...
    
    def _read_tasks(self) -> List[Task]:
        """Read and parse tasks from JSON file.
        
        Returns:
            List of Task objects
            Empty list if file doesn't exist
            
        Raises:
            ValueError: If JSON is corrupted (after backup)
        """
        ...
    
    def _write_tasks(self, tasks: List[Task]) -> None:
        """Write tasks to JSON file atomically.
        
        Args:
            tasks: List of tasks to write
            
        Raises:
            IOError: If write fails
        """
        ...
    
    def _get_next_id(self, tasks: List[Task]) -> int:
        """Calculate next sequential ID.
        
        Args:
            tasks: Existing tasks
            
        Returns:
            max(task IDs) + 1, or 1 if tasks is empty
        """
        ...
    
    def _create_timestamp(self) -> str:
        """Create current timestamp in ISO 8601 UTC format.
        
        Returns:
            Timestamp string (e.g., "2025-11-19T10:30:00Z")
        """
        ...
```

## CLI Layer Contract

### CLI Entry Point

**Module**: `tasks_cli.__main__`

**Purpose**: Provide the main entry point for the `tasks` command.

```python
def main() -> int:
    """Main entry point for tasks CLI.
    
    Parses command-line arguments and dispatches to appropriate command handler.
    
    Returns:
        Exit code: 0 for success, 1 for error
        
    Side Effects:
        - Prints output to stdout (success messages, task lists)
        - Prints errors to stderr
        - May read/write ~/.tasks.json file
        
    Example Usage:
        # As installed command
        $ tasks add "Buy groceries"
        Task added: [1] Buy groceries
        
        # As Python module
        $ python -m tasks_cli add "Buy groceries"
        Task added: [1] Buy groceries
    """
    ...
```

### Command Handlers

**Module**: `tasks_cli.commands.add`

```python
def add_command(description: str) -> int:
    """Handle 'tasks add <description>' command.
    
    Args:
        description: Task description from command line
        
    Returns:
        Exit code: 0 for success, 1 for error
        
    Side Effects:
        - Creates task in storage
        - Prints success message to stdout
        - Prints error to stderr on failure
        
    Example:
        >>> exit_code = add_command("Buy groceries")
        Task added: [1] Buy groceries
        >>> assert exit_code == 0
    """
    ...
```

**Module**: `tasks_cli.commands.list`

```python
def list_command() -> int:
    """Handle 'tasks list' command.
    
    Returns:
        Exit code: 0 for success, 1 for error
        
    Side Effects:
        - Reads tasks from storage
        - Prints tasks to stdout (sorted alphabetically)
        - Prints "No tasks found" if empty
        - Prints error to stderr on failure
        
    Example:
        >>> exit_code = list_command()
        [1] Buy groceries
        [2] Call dentist
        >>> assert exit_code == 0
    """
    ...
```

## Model Layer Contract

### Task Model

**Module**: `tasks_cli.models.task`

See [data-model.md](../data-model.md) for complete Task class definition.

**Key Contract Points**:

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class Task:
    """Immutable task representation.
    
    Contract:
        - All fields required except status (defaults to "pending")
        - Validation in __post_init__
        - Serialization via to_dict()
        - Deserialization via from_dict()
    """
    id: int
    description: str
    timestamp: str
    status: Literal["pending"] = "pending"
    
    def to_dict(self) -> dict:
        """Serialize to dict. MUST match storage schema."""
        ...
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize from dict. MUST handle schema evolution."""
        ...
```

## Command-Line Interface Contract

### Argument Parsing

**Command Structure**:
```
tasks <subcommand> [arguments]
```

**Available Subcommands**:

#### `add`

```bash
tasks add <description>
```

**Arguments**:
- `description` (required): Task description (quoted if contains spaces)

**Exit Codes**:
- `0`: Task added successfully
- `1`: Error (empty description, file error, etc.)

**Output Format** (stdout):
```
Task added: [<id>] <description>
```

**Error Format** (stderr):
```
Error: <error message>
```

**Examples**:
```bash
# Success
$ tasks add "Buy groceries"
Task added: [1] Buy groceries
$ echo $?
0

# Error: empty description
$ tasks add ""
Error: Task description cannot be empty
$ echo $?
1

# Error: unquoted description with spaces
$ tasks add Buy groceries
Error: Unrecognized arguments: groceries
$ echo $?
1
```

#### `list`

```bash
tasks list
```

**Arguments**: None

**Exit Codes**:
- `0`: Success (even if list is empty)
- `1`: Error (file read error, etc.)

**Output Format** (stdout):

*When tasks exist:*
```
[<id>] <description>
[<id>] <description>
...
```

*When no tasks:*
```
No tasks found
```

**Sorting**: Alphabetical by description, case-insensitive

**Examples**:
```bash
# With tasks
$ tasks list
[1] Buy groceries
[3] Call dentist
[2] Write documentation
$ echo $?
0

# No tasks
$ tasks list
No tasks found
$ echo $?
0

# Error (file permission issue)
$ tasks list
Error: Permission denied: /home/user/.tasks.json
$ echo $?
1
```

### Help System

```bash
# General help
$ tasks --help
# Shows: available commands, usage, options

# Command-specific help
$ tasks add --help
# Shows: add command usage, arguments, examples

$ tasks list --help
# Shows: list command usage, options, examples
```

## Error Handling Contract

### Error Categories

**Validation Errors** (User Input):
- Empty description → "Task description cannot be empty"
- Too long description → "Task description too long (X characters). Maximum is 1000 characters."
- Invalid arguments → "Unrecognized arguments: ..."

**Storage Errors** (File I/O):
- File permission denied → "Permission denied: <path>"
- Disk full → "No space left on device"
- Corrupted file → "Tasks file is corrupted. Backed up to <path>. Starting with empty task list."

**System Errors** (Unexpected):
- All other exceptions → "An unexpected error occurred: <message>"

### Error Handling Pattern

```python
def command_handler():
    try:
        # Normal operation
        ...
    except ValueError as e:
        # User input validation error
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except IOError as e:
        # File I/O error
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        # Unexpected error
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return 1
```

## Contract Testing

### Unit Test Contracts

```python
# Test: TaskStorage.add_task contract
def test_add_task_assigns_sequential_id():
    """Verify sequential ID assignment."""
    storage = TaskStorage(tmp_path / "test.json")
    task1 = storage.add_task("First")
    task2 = storage.add_task("Second")
    assert task1.id == 1
    assert task2.id == 2

def test_add_task_validates_description():
    """Verify description validation."""
    storage = TaskStorage(tmp_path / "test.json")
    with pytest.raises(ValueError, match="cannot be empty"):
        storage.add_task("")

def test_get_all_tasks_returns_list():
    """Verify return type is always list."""
    storage = TaskStorage(tmp_path / "test.json")
    tasks = storage.get_all_tasks()
    assert isinstance(tasks, list)
```

### Integration Test Contracts

```python
# Test: End-to-end add then list
def test_add_then_list_workflow():
    """Verify tasks persist and list correctly."""
    storage_path = tmp_path / "test.json"
    
    # Add tasks
    storage = TaskStorage(storage_path)
    storage.add_task("Zebra")
    storage.add_task("Apple")
    
    # List tasks (should be sorted)
    tasks = storage.get_all_tasks()
    # Sort for display
    sorted_tasks = sorted(tasks, key=lambda t: t.description.lower())
    
    assert sorted_tasks[0].description == "Apple"
    assert sorted_tasks[1].description == "Zebra"
```

## Backward Compatibility

### JSON Schema Compatibility

**Current Version (v1)**:
```json
[
  {"id": 1, "description": "...", "timestamp": "...", "status": "pending"}
]
```

**Future Version (v2)** - Must read v1:
```json
{
  "version": 2,
  "tasks": [
    {"id": 1, "description": "...", "timestamp": "...", "status": "pending", "tags": []}
  ]
}
```

**Compatibility Requirement**: v2 code MUST be able to read and migrate v1 files automatically.

### CLI Compatibility

**Guarantee**: Adding new commands MUST NOT break existing commands.

**Example**:
```bash
# v1
tasks add "..."
tasks list

# v2 (adds delete command)
tasks add "..."      # Still works
tasks list           # Still works  
tasks delete 1       # New command
```

## Performance Contracts

### Response Time Guarantees

| Operation | Maximum Time | Typical Time |
|-----------|-------------|--------------|
| `tasks add` | < 100ms | ~ 10ms |
| `tasks list` (< 100 tasks) | < 200ms | ~ 20ms |
| `tasks list` (< 1000 tasks) | < 500ms | ~ 100ms |

### Resource Limits

| Resource | Limit | Rationale |
|----------|-------|-----------|
| Task description | 1000 chars | Reasonable for CLI display |
| Total tasks | 10,000 | JSON file remains manageable |
| Memory footprint | < 50 MB | Lightweight CLI tool |
| Storage file size | < 5 MB | ~10k tasks avg 500 bytes each |

## Contract Verification

### How to Verify Contracts

```bash
# Run contract tests
pytest tests/contract/

# Run all tests with coverage
pytest --cov=tasks_cli --cov-fail-under=80

# Type checking
mypy src/tasks_cli/

# Linting
ruff check src/tasks_cli/
```

### Continuous Verification

All contracts MUST be verified in CI/CD pipeline before merge:
1. ✅ Unit tests pass
2. ✅ Integration tests pass
3. ✅ Contract tests pass
4. ✅ Type checking passes
5. ✅ Linting passes
6. ✅ Coverage ≥ 80%

---

**Contract Status**: Complete and ready for implementation
