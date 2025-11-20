# Data Model: Task Management CLI

**Feature**: Task Management CLI  
**Date**: 2025-11-19  
**Phase**: Phase 1 - Design

## Overview

This document defines the data model for the task management CLI. The model is intentionally simple for the MVP, focusing on the core Task entity and its storage representation.

## Entities

### Task

**Description**: Represents a single task item with a description, unique identifier, timestamp, and status.

**Attributes**:

| Attribute | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `id` | int | Yes | > 0, unique, sequential | Sequential integer starting from 1 |
| `description` | str | Yes | 1-1000 characters, non-empty | Text content of the task |
| `timestamp` | str | Yes | ISO 8601 format | When the task was created (UTC) |
| `status` | str | Yes | Must be "pending" | Current status (extensible in future) |

**Business Rules**:
1. **Unique IDs**: Each task must have a unique sequential integer ID
2. **ID Assignment**: IDs are assigned automatically by storage layer (not user-provided)
3. **ID Sequencing**: New tasks get `max(existing_ids) + 1`, starting from 1 if no tasks exist
4. **Description Validation**: Must be non-empty after stripping whitespace
5. **Description Length**: Maximum 1000 characters (enforced at storage layer)
6. **Timestamp Format**: ISO 8601 UTC (e.g., "2025-11-19T10:30:00Z")
7. **Status Values**: Only "pending" in MVP (future: "completed", "in-progress", "archived")
8. **Immutability**: In MVP, tasks cannot be modified or deleted once created

**Relationships**:
- None in MVP (tasks are independent entities)
- Future: May relate to projects, tags, or subtasks

**State Transitions**:
```
[Create] ────> [pending]
                   │
                   │ (Future: mark complete)
                   ├───> [completed]
                   │
                   │ (Future: archive)
                   └───> [archived]
```

### Python Representation

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

@dataclass
class Task:
    """Represents a single task item.
    
    Attributes:
        id: Sequential integer identifier starting from 1
        description: Text content of the task (1-1000 characters)
        timestamp: ISO 8601 timestamp when task was created (UTC)
        status: Current status (only 'pending' in MVP, extensible)
        
    Example:
        >>> task = Task(
        ...     id=1,
        ...     description="Buy groceries",
        ...     timestamp="2025-11-19T10:30:00Z",
        ...     status="pending"
        ... )
    """
    id: int
    description: str
    timestamp: str  # ISO 8601 format
    status: Literal["pending"] = "pending"
    
    def __post_init__(self):
        """Validate task attributes after initialization."""
        if self.id < 1:
            raise ValueError(f"Task ID must be positive, got {self.id}")
        
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        
        if len(self.description) > 1000:
            raise ValueError(
                f"Task description too long ({len(self.description)} chars), "
                f"maximum is 1000 characters"
            )
        
        # Basic ISO 8601 format validation
        try:
            datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(
                f"Invalid timestamp format: {self.timestamp}. "
                f"Expected ISO 8601 (e.g., '2025-11-19T10:30:00Z')"
            )
    
    def to_dict(self) -> dict:
        """Serialize task to dictionary for JSON storage.
        
        Returns:
            Dictionary representation suitable for JSON serialization
            
        Example:
            >>> task.to_dict()
            {
                'id': 1,
                'description': 'Buy groceries',
                'timestamp': '2025-11-19T10:30:00Z',
                'status': 'pending'
            }
        """
        return {
            "id": self.id,
            "description": self.description,
            "timestamp": self.timestamp,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize task from dictionary.
        
        Args:
            data: Dictionary with task fields
            
        Returns:
            Task instance
            
        Raises:
            KeyError: If required fields are missing
            ValueError: If field values are invalid
            
        Example:
            >>> data = {
            ...     'id': 1,
            ...     'description': 'Buy groceries',
            ...     'timestamp': '2025-11-19T10:30:00Z',
            ...     'status': 'pending'
            ... }
            >>> task = Task.from_dict(data)
        """
        return cls(
            id=data["id"],
            description=data["description"],
            timestamp=data["timestamp"],
            status=data.get("status", "pending")  # Default for backward compat
        )
    
    def __str__(self) -> str:
        """Human-readable string representation for display.
        
        Returns:
            Formatted string for CLI output
            
        Example:
            >>> print(task)
            [1] Buy groceries
        """
        return f"[{self.id}] {self.description}"
```

## Storage Schema

### JSON File Structure

**File Location**: `~/.tasks.json` (user's home directory)

**Format**: JSON array of task objects

**Schema**:
```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "timestamp": "2025-11-19T10:30:00Z",
    "status": "pending"
  },
  {
    "id": 2,
    "description": "Meeting at 3pm",
    "timestamp": "2025-11-19T11:15:00Z",
    "status": "pending"
  },
  {
    "id": 3,
    "description": "Write documentation",
    "timestamp": "2025-11-19T14:00:00Z",
    "status": "pending"
  }
]
```

**Schema Rules**:
1. **Root**: Array of task objects (not object with tasks property)
2. **Empty State**: Empty array `[]` (not null or missing file)
3. **Order**: Storage order doesn't matter (CLI handles sorting)
4. **Formatting**: Pretty-printed with 2-space indent for human readability

### Schema Evolution Strategy

**Current Version**: v1 (implicit, no version field)

**Future Versions**:
```json
{
  "version": 2,
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "timestamp": "2025-11-19T10:30:00Z",
      "status": "pending",
      "tags": ["personal", "urgent"],
      "due_date": "2025-11-20"
    }
  ]
}
```

**Migration Strategy**:
- Detect schema version (if no "version" field, assume v1)
- Auto-migrate on read (v1 → v2) with sensible defaults
- Write in latest version
- Maintain backward compatibility (v2 reader can read v1)

## Data Operations

### Create (Add Task)

**Input**: Task description (string)
**Process**:
1. Validate description (non-empty, ≤1000 chars)
2. Read existing tasks from file
3. Calculate next ID: `max(task.id for task in tasks) + 1` (or 1 if empty)
4. Generate timestamp: `datetime.now(UTC).isoformat() + "Z"`
5. Create Task object with id, description, timestamp, status="pending"
6. Append to task list
7. Write atomically to file
8. Return created task

**Output**: Created Task object

### Read (Get All Tasks)

**Input**: None
**Process**:
1. Read JSON file (handle file not found → empty list)
2. Parse JSON (handle corruption → backup + empty list)
3. Deserialize each object to Task instance
4. Validate each task (skip invalid with warning)
5. Return list of tasks

**Output**: List of Task objects (possibly empty)

### Sort (for Display)

**Input**: List of Task objects
**Process**:
1. Sort by description (case-insensitive alphabetical)
2. Implementation: `sorted(tasks, key=lambda t: t.description.lower())`

**Output**: Sorted list of Task objects

**Example**:
```python
# Input tasks (IDs: 3, 1, 2)
tasks = [
    Task(3, "zebra task", ...),
    Task(1, "Apple task", ...),
    Task(2, "banana TASK", ...)
]

# After sorting (case-insensitive alphabetical by description)
sorted_tasks = [
    Task(1, "Apple task", ...),      # 'a' comes first
    Task(2, "banana TASK", ...),     # 'b' comes second
    Task(3, "zebra task", ...)       # 'z' comes third
]
```

## Validation Rules

### Description Validation

```python
def validate_description(description: str) -> str:
    """Validate and normalize task description.
    
    Args:
        description: Raw description input
        
    Returns:
        Normalized description (stripped whitespace)
        
    Raises:
        ValueError: If description is invalid
    """
    # Strip leading/trailing whitespace
    normalized = description.strip()
    
    # Check not empty
    if not normalized:
        raise ValueError("Task description cannot be empty")
    
    # Check length
    if len(normalized) > 1000:
        raise ValueError(
            f"Task description too long ({len(normalized)} characters). "
            f"Maximum is 1000 characters."
        )
    
    return normalized
```

### ID Validation

```python
def validate_id(task_id: int) -> int:
    """Validate task ID.
    
    Args:
        task_id: Task ID to validate
        
    Returns:
        Validated ID
        
    Raises:
        ValueError: If ID is invalid
    """
    if not isinstance(task_id, int):
        raise ValueError(f"Task ID must be integer, got {type(task_id)}")
    
    if task_id < 1:
        raise ValueError(f"Task ID must be positive, got {task_id}")
    
    return task_id
```

### Timestamp Validation

```python
from datetime import datetime

def validate_timestamp(timestamp: str) -> str:
    """Validate ISO 8601 timestamp.
    
    Args:
        timestamp: Timestamp string to validate
        
    Returns:
        Validated timestamp
        
    Raises:
        ValueError: If timestamp is invalid
    """
    try:
        # Parse ISO 8601 (handle 'Z' suffix)
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return timestamp
    except ValueError as e:
        raise ValueError(
            f"Invalid timestamp format: {timestamp}. "
            f"Expected ISO 8601 (e.g., '2025-11-19T10:30:00Z')"
        ) from e
```

## Example Data Flows

### Add Task Flow

```
User Input: "Buy groceries"
    ↓
Validate description
    ↓
Read existing tasks from ~/.tasks.json
    ├─ File exists: [{id: 1, ...}, {id: 2, ...}]
    └─ File missing: []
    ↓
Calculate next ID: 3 (or 1 if empty)
    ↓
Generate timestamp: "2025-11-19T10:30:00Z"
    ↓
Create Task object:
    Task(id=3, description="Buy groceries", 
         timestamp="2025-11-19T10:30:00Z", status="pending")
    ↓
Append to task list: [task1, task2, task3]
    ↓
Serialize to JSON and write atomically
    ↓
Output: "Task added: [3] Buy groceries"
```

### List Tasks Flow

```
User Command: "tasks list"
    ↓
Read tasks from ~/.tasks.json
    ├─ File exists & valid: Parse JSON → [task1, task2, task3]
    ├─ File exists & corrupted: Backup → [] (empty list)
    └─ File missing: []
    ↓
Check if empty
    ├─ Empty: Output "No tasks found"
    └─ Not empty: Continue
    ↓
Sort tasks (case-insensitive alphabetical by description)
    ↓
Format for display:
    [1] Apple task
    [3] Buy groceries  
    [2] Zebra task
    ↓
Output to console
```

## Data Integrity

### Corruption Prevention
1. **Atomic Writes**: Write to temp file → rename (atomic operation)
2. **Validation**: Validate all data before writing
3. **Backup**: On corruption detection, backup old file before recovery

### Corruption Recovery
1. **Detection**: Catch `json.JSONDecodeError` on read
2. **Backup**: Copy corrupted file to `.tasks.json.backup`
3. **Recovery**: Start with empty task list, inform user
4. **Logging**: Log error with corruption details

### Data Loss Prevention
1. **Atomic writes** prevent partial writes
2. **Validation** prevents invalid data from being written
3. **Backup on corruption** preserves data for manual recovery

## Testing Considerations

### Unit Tests
- Task model validation (empty, too long, valid)
- Task serialization/deserialization
- ID calculation (empty list, existing tasks)
- Sorting (case-insensitive, various descriptions)

### Integration Tests
- File operations (create, read, write)
- Corruption recovery (manually corrupt file, verify recovery)
- Edge cases (permissions, disk full, concurrent access)

### Contract Tests
- Storage interface compliance
- Task model interface compliance

## Future Enhancements

### Additional Entities (Out of Scope for MVP)
- **Tag**: Categorize tasks (e.g., "work", "personal", "urgent")
- **Project**: Group related tasks
- **Subtask**: Break down tasks into smaller pieces
- **User**: Multi-user support (local or cloud sync)

### Additional Attributes
- `due_date`: When task should be completed
- `priority`: High, Medium, Low
- `completed_at`: Timestamp when marked complete
- `notes`: Additional details/context
- `recurrence`: For recurring tasks

### Relationships
```python
@dataclass
class Task:
    # ... existing fields ...
    project_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    tags: List[str] = field(default_factory=list)
```

**Status**: Data model complete and ready for implementation
