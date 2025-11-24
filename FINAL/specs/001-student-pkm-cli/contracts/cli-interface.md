# CLI Interface Contracts

**Phase**: 1 - Design & Contracts  
**Date**: 2025-11-23  
**For**: Implementation Plan `plan.md`

## Overview

This document defines the command-line interface contracts for the Student PKM CLI. All commands follow Click framework conventions with auto-generated help, consistent error formatting (rich), and structured output.

---

## Global Options

Available for all commands:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--data-dir` | Path | `~/.pkm/` | Override data directory location |
| `--no-color` | flag | False | Disable colored output |
| `--verbose` | flag | False | Enable debug logging |
| `--help` | flag | - | Show help and exit |

**Example**:
```bash
pkm --data-dir ~/custom/path view inbox
pkm --no-color view tasks  # For CI/scripting
```

---

## Command Groups

### 1. Quick Capture Commands (`add`)

#### `pkm add note [CONTENT]`

**Purpose**: Capture a note with optional interactive mode.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `CONTENT` | str | No* | Note content (multi-line if in quotes) |

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--interactive`, `-i` | flag | False | Open text editor for long-form content |
| `--course`, `-c` | str | None | Assign to course immediately |
| `--topics`, `-t` | str (CSV) | None | Add topics (comma-separated) |

**Behavior**:
- If `CONTENT` provided: Create note directly
- If `--interactive`: Open $EDITOR for content input
- If neither: Prompt for content interactively
- Auto-generate ID and timestamp
- Return note ID and success message

**Output** (success):
```
✓ Note created: n_20251123_103045_a7c
  Course: Biology 101
  Topics: Photosynthesis, Cell Structure
```

**Output** (error):
```
✗ Error: Content cannot be empty
```

**Examples**:
```bash
# Quick capture to inbox
pkm add note "Remember to review chapter 5"

# With course and topics
pkm add note "Photosynthesis equation" -c "Biology 101" -t "Photosynthesis, Cell Structure"

# Interactive mode (opens $EDITOR)
pkm add note -i -c "Biology 101"

# Multi-line (quote properly in shell)
pkm add note "Line 1
Line 2
Line 3"
```

**Exit Codes**:
- `0`: Success
- `1`: Validation error (empty content, invalid course/topic format)
- `2`: Storage error (permission denied, disk full)

---

#### `pkm add task TITLE`

**Purpose**: Create a task with optional metadata.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TITLE` | str | Yes | Task description |

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--due`, `-d` | str | None | Due date (natural language or YYYY-MM-DD) |
| `--priority`, `-p` | choice | medium | Priority: high, medium, low |
| `--course`, `-c` | str | None | Assign to course |
| `--link-note`, `-n` | str (repeatable) | [] | Link to note IDs |

**Behavior**:
- Parse `--due` with python-dateutil (supports "tomorrow", "next Friday", "2025-12-01")
- Validate priority is one of [high, medium, low]
- Verify linked notes exist before creating task
- Auto-generate ID and timestamp

**Output** (success):
```
✓ Task created: t_20251123_140000_xyz
  Title: Submit lab report
  Due: Friday, Nov 25 at 11:59 PM (2 days)
  Priority: high
  Course: Biology 101
  Linked notes: n_20251123_103045_a7c
```

**Output** (error):
```
✗ Error: Note 'n_invalid_id' not found
```

**Examples**:
```bash
# Quick task to inbox
pkm add task "Buy textbook"

# Full metadata
pkm add task "Submit lab report" -d "Friday 11:59pm" -p high -c "Biology 101" -n n_20251123_103045_a7c

# Multiple linked notes
pkm add task "Study for exam" -n n_123 -n n_456 -n n_789
```

**Exit Codes**: Same as `add note`

---

### 2. View Commands (`view`)

#### `pkm view inbox`

**Purpose**: Display uncategorized notes and tasks.

**Arguments**: None

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--type`, `-t` | choice | all | Filter: all, notes, tasks |

**Output**:
```
📥 INBOX (5 notes, 3 tasks)

NOTES (5)
─────────────────────────────────────────
n_20251123_103045_a7c  2 hours ago
Remember to review chapter 5

n_20251123_090000_def  5 hours ago
Ideas for research paper topic
─────────────────────────────────────────

TASKS (3)
─────────────────────────────────────────
t_20251123_140000_xyz  [HIGH] Due Friday, Nov 25
Buy textbook for new semester

t_20251122_100000_abc  [MEDIUM] Due tomorrow
Review lecture notes
─────────────────────────────────────────
```

**Example**:
```bash
pkm view inbox              # All items
pkm view inbox --type notes # Notes only
pkm view inbox -t tasks     # Tasks only
```

**Exit Codes**: `0` (always succeeds, shows empty message if no items)

---

#### `pkm view tasks`

**Purpose**: Display filtered task list.

**Arguments**: None

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--filter`, `-f` | choice | all | Filter: all, today, week, overdue |
| `--priority`, `-p` | choice | None | Filter by priority: high, medium, low |
| `--course`, `-c` | str | None | Filter by course name |
| `--completed` | flag | False | Show completed tasks |

**Output**:
```
📋 TASKS (8 active, 12 completed)

TODAY (2)
─────────────────────────────────────────
t_123  [HIGH] Due today at 11:59 PM
Submit lab report on photosynthesis
Biology 101 · 2/3 subtasks done
Linked: n_456

t_456  [MEDIUM] Due today at 5:00 PM
Review chapter 5 notes
Biology 101
─────────────────────────────────────────

THIS WEEK (3)
... (similar format)

OVERDUE (1)
... (similar format, highlighted red)
```

**Examples**:
```bash
pkm view tasks                     # All active tasks
pkm view tasks -f today            # Due today
pkm view tasks -f week             # Due this week
pkm view tasks -f overdue          # Past due
pkm view tasks -p high             # High priority only
pkm view tasks -c "Biology 101"    # Course filter
pkm view tasks --completed         # Show completed
```

**Exit Codes**: `0`

---

#### `pkm view course COURSE_NAME`

**Purpose**: Display all notes and tasks for a specific course.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `COURSE_NAME` | str | Yes | Course name (quoted if spaces) |

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--type`, `-t` | choice | all | Filter: all, notes, tasks |

**Output**:
```
📚 Biology 101 (15 notes, 8 tasks)

TOPICS
Photosynthesis (5), Cell Structure (7), Genetics (3)

NOTES (15, showing 5 most recent)
─────────────────────────────────────────
n_123  2 hours ago · Photosynthesis, Cell Structure
Photosynthesis equation and process notes

n_456  1 day ago · Genetics
Punnett square examples
─────────────────────────────────────────

TASKS (8 active)
─────────────────────────────────────────
t_789  [HIGH] Due Friday · 2/3 subtasks
Submit lab report on photosynthesis
Linked: n_123

t_012  [MEDIUM] Due next week
Study for midterm exam
─────────────────────────────────────────

View all: pkm search --course "Biology 101"
```

**Examples**:
```bash
pkm view course "Biology 101"
pkm view course Math -t notes      # Notes only
```

**Exit Codes**:
- `0`: Success
- `1`: Course not found

---

#### `pkm view note NOTE_ID`

**Purpose**: Display full note details.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `NOTE_ID` | str | Yes | Note identifier |

**Output**:
```
📝 Note: n_20251123_103045_a7c

CONTENT
─────────────────────────────────────────
Photosynthesis converts light energy to chemical energy

Key equation:
6CO2 + 6H2O → C6H12O6 + 6O2

Process stages:
1. Light reactions (thylakoid)
2. Calvin cycle (stroma)
─────────────────────────────────────────

METADATA
Created:  Nov 23, 2025 at 10:30 AM
Modified: Nov 23, 2025 at 10:30 AM
Course:   Biology 101
Topics:   Photosynthesis, Cell Structure

LINKED TASKS (1)
t_789  [HIGH] Due Friday
Submit lab report on photosynthesis
```

**Examples**:
```bash
pkm view note n_20251123_103045_a7c
```

**Exit Codes**:
- `0`: Success
- `1`: Note not found

---

#### `pkm view task TASK_ID`

**Purpose**: Display full task details with subtasks.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TASK_ID` | str | Yes | Task identifier |

**Output**:
```
✓ Task: t_20251123_140000_xyz

DETAILS
─────────────────────────────────────────
Title:    Submit lab report on photosynthesis
Status:   Active
Due:      Friday, Nov 25 at 11:59 PM (in 2 days)
Priority: high
Course:   Biology 101
Created:  Nov 23, 2025 at 2:00 PM
─────────────────────────────────────────

SUBTASKS (2/3 completed)
☑ 1. Review notes from lecture
☑ 2. Complete data analysis
☐ 3. Write conclusion section

LINKED NOTES (1)
n_456  2 hours ago
Photosynthesis equation and process notes
```

**Examples**:
```bash
pkm view task t_20251123_140000_xyz
```

**Exit Codes**:
- `0`: Success
- `1`: Task not found

---

### 3. Organization Commands (`organize`)

#### `pkm organize note NOTE_ID`

**Purpose**: Move note to course or update topics.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `NOTE_ID` | str | Yes | Note identifier |

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course`, `-c` | str | None | Move to course (use "inbox" for None) |
| `--add-topics`, `-t` | str (CSV) | None | Add topics |
| `--remove-topic`, `-r` | str (repeatable) | [] | Remove topics |

**Output** (success):
```
✓ Note organized: n_20251123_103045_a7c
  Moved to: Biology 101
  Added topics: Cell Structure
  Removed topics: Draft
```

**Examples**:
```bash
# Move to course
pkm organize note n_123 -c "Biology 101"

# Move to inbox
pkm organize note n_123 -c inbox

# Add topics
pkm organize note n_123 -t "Photosynthesis, Cell Structure"

# Remove topic
pkm organize note n_123 -r "Draft"

# Combined
pkm organize note n_123 -c "Biology 101" -t "Photosynthesis" -r "Draft"
```

**Exit Codes**:
- `0`: Success
- `1`: Note not found or validation error

---

#### `pkm organize task TASK_ID`

**Purpose**: Move task to course or update metadata.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TASK_ID` | str | Yes | Task identifier |

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course`, `-c` | str | None | Move to course (use "inbox" for None) |
| `--due`, `-d` | str | None | Update due date |
| `--priority`, `-p` | choice | None | Update priority |

**Output** (success):
```
✓ Task organized: t_20251123_140000_xyz
  Moved to: Biology 101
  Due date: Friday, Nov 25 at 11:59 PM
  Priority: high
```

**Examples**:
```bash
pkm organize task t_123 -c "Biology 101"
pkm organize task t_123 -d "next Friday" -p high
```

**Exit Codes**: Same as `organize note`

---

### 4. Task Management Commands (`task`)

#### `pkm task complete TASK_ID`

**Purpose**: Mark task as completed.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TASK_ID` | str | Yes | Task identifier |

**Output**:
```
✓ Task completed: t_20251123_140000_xyz
  Completed at: Nov 23, 2025 at 3:45 PM
  Time to complete: 1 day, 1 hour
```

**Examples**:
```bash
pkm task complete t_123
```

**Exit Codes**:
- `0`: Success
- `1`: Task not found or already completed

---

#### `pkm task uncomplete TASK_ID`

**Purpose**: Reopen a completed task.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TASK_ID` | str | Yes | Task identifier |

**Output**:
```
✓ Task reopened: t_20251123_140000_xyz
```

**Examples**:
```bash
pkm task uncomplete t_123
```

**Exit Codes**: Same as `task complete`

---

#### `pkm task add-subtask TASK_ID TITLE`

**Purpose**: Add a subtask to an existing task.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TASK_ID` | str | Yes | Parent task identifier |
| `TITLE` | str | Yes | Subtask description |

**Output**:
```
✓ Subtask added to t_123
  #4: Review chapter 6
```

**Examples**:
```bash
pkm task add-subtask t_123 "Review chapter 6"
```

**Exit Codes**:
- `0`: Success
- `1`: Task not found or validation error

---

#### `pkm task complete-subtask TASK_ID SUBTASK_ID`

**Purpose**: Mark a subtask as completed.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TASK_ID` | str | Yes | Parent task identifier |
| `SUBTASK_ID` | int | Yes | Subtask number (1, 2, 3...) |

**Output**:
```
✓ Subtask completed: #2
  Progress: 2/3 subtasks done (67%)
```

**Examples**:
```bash
pkm task complete-subtask t_123 2
```

**Exit Codes**:
- `0`: Success
- `1`: Task or subtask not found

---

#### `pkm task link-note TASK_ID NOTE_ID`

**Purpose**: Link a note to a task for context.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `TASK_ID` | str | Yes | Task identifier |
| `NOTE_ID` | str | Yes | Note identifier |

**Output**:
```
✓ Linked note to task
  Task: t_123 - Submit lab report
  Note: n_456 - Photosynthesis notes
```

**Examples**:
```bash
pkm task link-note t_123 n_456
```

**Exit Codes**:
- `0`: Success
- `1`: Task or note not found, or link already exists

---

### 5. Search Commands (`search`)

#### `pkm search QUERY`

**Purpose**: Full-text search across notes and tasks.

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `QUERY` | str | Yes | Search keywords |

**Options**:
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--type`, `-t` | choice | all | Filter: all, notes, tasks |
| `--course`, `-c` | str | None | Search within course only |
| `--topic` | str | None | Search within topic only |
| `--limit`, `-l` | int | 20 | Max results to show |

**Behavior**:
- Case-insensitive substring match on content/title
- Shows relevance (exact match > prefix match > substring)
- Highlights matching text in output

**Output**:
```
🔍 Search results for "photosynthesis" (3 matches)

NOTES (2)
─────────────────────────────────────────
n_123  Biology 101 · 2 hours ago
**Photosynthesis** converts light energy to chemical...

n_456  Biology 101 · 1 day ago
Key equation for **photosynthesis**: 6CO2 + 6H2O → ...
─────────────────────────────────────────

TASKS (1)
─────────────────────────────────────────
t_789  [HIGH] Due Friday · Biology 101
Submit lab report on **photosynthesis**
─────────────────────────────────────────
```

**Examples**:
```bash
pkm search "photosynthesis"
pkm search "equation" -t notes
pkm search "exam" -c "Biology 101"
pkm search "cell" --topic "Cell Structure"
pkm search "study" -l 10  # Limit to 10 results
```

**Exit Codes**:
- `0`: Success (even if no results)
- `1`: Validation error (invalid course/topic)

---

### 6. Help & System Commands

#### `pkm --version`

**Purpose**: Show version information.

**Output**:
```
Pro Study Planner v1.0.0
Python 3.11+ · uv package manager
Data directory: /Users/student/.pkm/
```

---

#### `pkm help [COMMAND]`

**Purpose**: Show help for specific command (Click auto-generated).

**Examples**:
```bash
pkm help               # General help
pkm help add           # Help for 'add' group
pkm help add note      # Help for 'add note' command
```

---

## Error Handling

All commands follow consistent error formatting:

**Format**:
```
✗ Error: {error_message}
  {optional_context}

Suggestion: {helpful_next_step}
```

**Common Errors**:

| Error | Exit Code | Example |
|-------|-----------|---------|
| Not found | 1 | `✗ Error: Note 'n_invalid' not found` |
| Validation error | 1 | `✗ Error: Content cannot be empty` |
| Storage error | 2 | `✗ Error: Permission denied: ~/.pkm/data.json` |
| Invalid argument | 1 | `✗ Error: Priority must be one of: high, medium, low` |

---

## Output Formatting

All output uses `rich` library for:
- **Colors**: High priority = red, medium = yellow, low = blue
- **Icons**: ✓ (success), ✗ (error), 📝 (note), ✓ (task), 📚 (course), 🔍 (search)
- **Tables**: For multi-item views (inbox, tasks, search)
- **Progress**: Subtask completion bars

**Accessibility**: `--no-color` flag disables all formatting for screen readers and CI.

---

## Performance Targets

Per `plan.md` Constitution Check:

| Command | Target | Rationale |
|---------|--------|-----------|
| `pkm add note` | < 200ms | User perceives as instant |
| `pkm view inbox` | < 500ms | With 500 tasks, 1000 notes |
| `pkm search {query}` | < 1s | Full-text across all data |
| Startup (`pkm --help`) | < 1s | No data loading needed |

---

## JSON Schema Validation

For programmatic use, all entities can be exported as JSON:

**Example**: `pkm export --format json > data.json`

See `contracts/json-schemas/` for validation rules (optional future feature).

---

## Summary

**Command Groups**: add, view, organize, task, search  
**Total Commands**: 15 core commands  
**Common Patterns**: Consistent `--course`, `--type` filters across views  
**Error Handling**: Rich formatting, helpful suggestions, predictable exit codes  
**Performance**: <1s for all commands per Constitution Check

**Next**: See `quickstart.md` for common workflows and usage examples.
