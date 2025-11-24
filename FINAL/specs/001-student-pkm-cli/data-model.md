# Data Model: Pro Study Planner

**Phase**: 1 - Data Model Design  
**Date**: 2025-11-23  
**For**: Implementation Plan `plan.md`

## Overview

This document defines the conceptual data model for the Pro Study Planner. All entities are implemented as Pydantic models for type safety and runtime validation. The model supports the "quick capture, organize later" workflow with clear relationships between notes, tasks, courses, and topics.

---

## Entity Relationship Diagram

```
┌─────────────┐
│    Course   │
└──────┬──────┘
       │ 1
       │
       │ *
    ┌──┴───┐
    │      │
┌───▼──┐ ┌─▼────┐       ┌──────────┐
│ Note │ │ Task │◄──────┤ Subtask  │
└───┬──┘ └─┬─┬──┘   *   └──────────┘
    │      │ │
    │  link│ │
    │      │ │ *
    └──────┘ │
       *     │ *
    ┌────────▼───┐
    │   Topic    │
    └────────────┘

Special Containers:
┌─────────┐
│  Inbox  │ (virtual - notes/tasks with course=None)
└─────────┘
```

---

## Core Entities

### 1. Note

**Purpose**: Captures information, lecture notes, ideas, or references.

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | str | Yes | auto | Unique identifier (e.g., "n_20251123_103045_abc") |
| `content` | str | Yes | - | Note body text (multi-line supported) |
| `created_at` | datetime | Yes | now() | Timestamp when note was created |
| `modified_at` | datetime | Yes | now() | Last modification timestamp |
| `course` | str \| None | No | None | Course assignment (None = inbox) |
| `topics` | list[str] | No | [] | Topic tags for categorization |
| `linked_from_tasks` | list[str] | No | [] | Task IDs that reference this note |

**Validation Rules**:
- `content`: Must be non-empty, max 10,000 characters
- `id`: Must match pattern `n_[timestamp]_[random]`
- `topics`: Each topic must be 1-50 characters, alphanumeric + spaces
- `course`: If set, must be 1-100 characters

**Indexes** (for efficient queries):
- By `course` (for `view course`)
- By `topics` (for `search --topic`)
- By `id` (primary key)

**Example**:
```python
Note(
    id="n_20251123_103045_a7c",
    content="Photosynthesis converts light energy to chemical energy\nKey equation: 6CO2 + 6H2O → C6H12O6 + 6O2",
    created_at=datetime(2025, 11, 23, 10, 30, 45),
    modified_at=datetime(2025, 11, 23, 10, 30, 45),
    course="Biology 101",
    topics=["Photosynthesis", "Cell Structure"],
    linked_from_tasks=["t_20251123_140000_xyz"]
)
```

---

### 2. Task

**Purpose**: Represents an actionable item with optional deadline, priority, and subtasks.

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | str | Yes | auto | Unique identifier (e.g., "t_20251123_140000_xyz") |
| `title` | str | Yes | - | Task description |
| `created_at` | datetime | Yes | now() | Timestamp when task was created |
| `due_date` | datetime \| None | No | None | When task is due |
| `priority` | Literal["high", "medium", "low"] | No | "medium" | Task priority |
| `completed` | bool | No | False | Completion status |
| `completed_at` | datetime \| None | No | None | When task was marked complete |
| `course` | str \| None | No | None | Course assignment (None = inbox) |
| `linked_notes` | list[str] | No | [] | Note IDs providing context for this task |
| `subtasks` | list[Subtask] | No | [] | Nested subtasks |

**Validation Rules**:
- `title`: Must be non-empty, max 200 characters
- `id`: Must match pattern `t_[timestamp]_[random]`
- `due_date`: Must be valid datetime, can be in past (becomes overdue)
- `priority`: Must be one of ["high", "medium", "low"]
- `completed_at`: Can only be set if `completed` is True

**Computed Properties**:
- `is_overdue`: `due_date < now() and not completed`
- `is_due_today`: `due_date.date() == today()`
- `is_due_this_week`: `due_date <= today() + 7 days`
- `subtask_progress`: `(completed_subtasks / total_subtasks)` percentage

**Indexes** (for efficient queries):
- By `due_date` (for `view today`, `view week`, `view overdue`)
- By `course` (for `view course`)
- By `priority` (for `view tasks --priority`)
- By `id` (primary key)

**Example**:
```python
Task(
    id="t_20251123_140000_xyz",
    title="Submit lab report on photosynthesis",
    created_at=datetime(2025, 11, 23, 14, 0, 0),
    due_date=datetime(2025, 11, 25, 23, 59, 59),
    priority="high",
    completed=False,
    completed_at=None,
    course="Biology 101",
    linked_notes=["n_20251123_103045_a7c"],
    subtasks=[
        Subtask(id=1, title="Review notes", completed=True),
        Subtask(id=2, title="Write conclusion", completed=False)
    ]
)
```

---

### 3. Subtask

**Purpose**: Smaller actionable items nested under a parent task.

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | int | Yes | auto | Unique within parent task (1, 2, 3...) |
| `title` | str | Yes | - | Subtask description |
| `completed` | bool | No | False | Completion status |
| `created_at` | datetime | Yes | now() | Timestamp when subtask was created |

**Validation Rules**:
- `title`: Must be non-empty, max 200 characters
- `id`: Auto-incremented within parent task scope

**Note**: Subtasks are embedded within Task objects, not standalone entities.

**Example**:
```python
Subtask(
    id=1,
    title="Review chapter 5 notes",
    completed=True,
    created_at=datetime(2025, 11, 23, 14, 5, 0)
)
```

---

### 4. Course

**Purpose**: Organizational container for notes and tasks related to a class/subject.

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | str | Yes | - | Course identifier (e.g., "Biology 101") |
| `created_at` | datetime | Yes | now() | When course was first used |
| `note_count` | int | No | 0 | Cached count of notes (computed) |
| `task_count` | int | No | 0 | Cached count of tasks (computed) |

**Validation Rules**:
- `name`: Must be unique, 1-100 characters, non-empty
- Counts are computed from notes/tasks with `course=name`

**Indexes**:
- By `name` (primary key)

**Note**: Courses are auto-created when first referenced. No explicit "create course" command needed.

**Example**:
```python
Course(
    name="Biology 101",
    created_at=datetime(2025, 11, 20, 9, 0, 0),
    note_count=15,
    task_count=8
)
```

---

### 5. Topic

**Purpose**: Tag for categorizing notes within or across courses.

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | str | Yes | - | Topic label (e.g., "Photosynthesis") |
| `course` | str \| None | No | None | Course-specific topic (None = global) |
| `note_count` | int | No | 0 | Cached count of notes with this topic |

**Validation Rules**:
- `name`: 1-50 characters, alphanumeric + spaces
- Topics can be course-specific or global (reused across courses)

**Note**: Topics are auto-created when first used. No explicit management needed.

**Example**:
```python
Topic(
    name="Cell Structure",
    course="Biology 101",  # Course-specific
    note_count=5
)

Topic(
    name="Study Techniques",
    course=None,  # Global across all courses
    note_count=12
)
```

---

### 6. Inbox (Virtual Entity)

**Purpose**: Logical container for uncategorized notes and tasks.

**Implementation**: Not a separate entity. Items in inbox are those with `course=None`.

**Queries**:
- Inbox notes: `filter(notes, lambda n: n.course is None)`
- Inbox tasks: `filter(tasks, lambda t: t.course is None)`

---

## Data Storage Schema (JSON)

**File**: `~/.pkm/data.json`

```json
{
  "version": "1.0.0",
  "last_modified": "2025-11-23T14:30:00Z",
  "notes": [
    {
      "id": "n_20251123_103045_a7c",
      "content": "Photosynthesis converts light energy...",
      "created_at": "2025-11-23T10:30:45Z",
      "modified_at": "2025-11-23T10:30:45Z",
      "course": "Biology 101",
      "topics": ["Photosynthesis", "Cell Structure"],
      "linked_from_tasks": ["t_20251123_140000_xyz"]
    }
  ],
  "tasks": [
    {
      "id": "t_20251123_140000_xyz",
      "title": "Submit lab report on photosynthesis",
      "created_at": "2025-11-23T14:00:00Z",
      "due_date": "2025-11-25T23:59:59Z",
      "priority": "high",
      "completed": false,
      "completed_at": null,
      "course": "Biology 101",
      "linked_notes": ["n_20251123_103045_a7c"],
      "subtasks": [
        {
          "id": 1,
          "title": "Review notes",
          "completed": true,
          "created_at": "2025-11-23T14:05:00Z"
        }
      ]
    }
  ],
  "courses": [
    {
      "name": "Biology 101",
      "created_at": "2025-11-20T09:00:00Z",
      "note_count": 15,
      "task_count": 8
    }
  ],
  "topics": [
    {
      "name": "Photosynthesis",
      "course": "Biology 101",
      "note_count": 5
    }
  ]
}
```

---

## Relationships

### Note ↔ Task (Many-to-Many)

**Implementation**: 
- Task stores `linked_notes: list[str]` (note IDs)
- Note stores `linked_from_tasks: list[str]` (task IDs)
- Bidirectional sync maintained by `TaskService.link_note()`

**Usage**:
```python
# Link note to task
task_service.link_note(task_id="t_123", note_id="n_456")
# Updates: task.linked_notes += ["n_456"]
#          note.linked_from_tasks += ["t_123"]

# Unlink
task_service.unlink_note(task_id="t_123", note_id="n_456")
```

### Note/Task → Course (Many-to-One)

**Implementation**:
- Note/Task stores `course: str | None`
- Course `note_count` and `task_count` computed on demand

**Usage**:
```python
# Assign to course
note_service.organize(note_id="n_456", course="Biology 101")
# Auto-creates course if doesn't exist

# Move to inbox
note_service.organize(note_id="n_456", course=None)
```

### Note → Topics (Many-to-Many)

**Implementation**:
- Note stores `topics: list[str]`
- Topic entity tracks usage count

**Usage**:
```python
# Add topics
note_service.add_topics(note_id="n_456", topics=["Photosynthesis", "Cell Structure"])

# Remove topic
note_service.remove_topic(note_id="n_456", topic="Photosynthesis")
```

### Task → Subtasks (One-to-Many)

**Implementation**:
- Task stores `subtasks: list[Subtask]`
- Subtasks embedded in parent task (no separate IDs in global scope)

**Usage**:
```python
# Add subtask
task_service.add_subtask(task_id="t_123", title="Review chapter 1")
# Generates subtask.id = max(existing_ids) + 1

# Complete subtask
task_service.complete_subtask(task_id="t_123", subtask_id=1)
```

---

## ID Generation Strategy

**Format**: `{type}_{timestamp}_{random}`

**Components**:
- `type`: Single letter prefix (`n` = note, `t` = task)
- `timestamp`: YYYYMMDDHHmmss (sortable, roughly chronological)
- `random`: 3-character alphanumeric (collision avoidance)

**Example**: `n_20251123_103045_a7c`

**Properties**:
- **Unique**: Timestamp + random ensures no collisions
- **Sortable**: Chronological by default (latest first when sorted desc)
- **Short**: Easy to type for CLI (vs UUID)
- **Readable**: Prefix indicates type at a glance

**Implementation**:
```python
def generate_note_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    return f"n_{timestamp}_{random_suffix}"
```

---

## Computed Fields & Indexes

**For Performance** (per research.md):

### Note Indexes
```python
{
    "by_id": {"n_123": Note(...), "n_456": Note(...)},
    "by_course": {"Biology 101": [Note(...), Note(...)], None: [...]},
    "by_topic": {"Photosynthesis": [Note(...), ...]}
}
```

### Task Indexes
```python
{
    "by_id": {"t_123": Task(...), "t_456": Task(...)},
    "by_due_date": {date(2025, 11, 25): [Task(...), ...]},
    "by_course": {"Biology 101": [Task(...), ...], None: [...]},
    "by_priority": {"high": [Task(...), ...]}
}
```

**Recomputed**: On data load and after mutations. Cached in memory for session.

---

## Migration Strategy

**Version**: Stored in `data.json` as `"version": "1.0.0"`

**Future Migrations**:
```python
def migrate_1_0_to_1_1(data: dict) -> dict:
    """Example: Add new field with default value."""
    for note in data["notes"]:
        note.setdefault("new_field", default_value)
    data["version"] = "1.1.0"
    return data
```

**Backward Compatibility**: Old versions can read new data (ignore unknown fields via Pydantic `extra="ignore"`).

---

## Data Integrity Rules

1. **Referential Integrity**:
   - If task links to note, note must exist (or link removed)
   - If note/task references course, course auto-created if missing

2. **Consistency**:
   - Task.linked_notes ↔ Note.linked_from_tasks kept in sync
   - Course counts recomputed on load (don't trust cached values)

3. **Validation**:
   - All fields validated by Pydantic on load
   - Invalid data triggers backup + recovery process

4. **Atomic Updates**:
   - Write to `data.json.tmp` → rename to `data.json`
   - Old version backed up to `data.json.bak`
   - Prevents corruption from crashes mid-write

---

## Summary

**Entities**: Note, Task, Subtask, Course, Topic (+ virtual Inbox)

**Key Design Decisions**:
- Pydantic models for type safety + validation
- JSON storage for human readability
- Smart IDs (sortable, typed, short)
- Bidirectional relationships maintained by services
- Indexes for performance (<500ms filtered views)
- Atomic writes for data safety

**Next Steps**: See `contracts/` for JSON schema validation rules and API contracts for each entity.
