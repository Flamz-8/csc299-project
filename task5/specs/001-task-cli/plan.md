# Implementation Plan: Task Management CLI

**Branch**: `001-task-cli` | **Date**: 2025-11-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-task-cli/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a command-line task management application with two primary user stories: (P1) add tasks via `tasks add "description"` command, and (P2) list tasks via `tasks list` command. Tasks are stored persistently in a JSON file located in the user's home directory (~/.tasks.json). The implementation emphasizes logical separation between CLI and storage components, with sequential integer IDs for tasks and case-insensitive alphabetical sorting for display.

Technical approach: Python 3.14+ with uv for dependency management, pytest for testing, and standard library JSON for file operations. Architecture follows clear separation of concerns with distinct CLI and storage modules.

## Technical Context

**Language/Version**: Python 3.14+  
**Primary Dependencies**: uv (project/dependency management), pytest (testing framework)  
**Storage**: JSON file in user's home directory (~/.tasks.json)  
**Testing**: pytest with pytest-cov for coverage reporting  
**Target Platform**: Cross-platform (Windows, macOS, Linux) - any system with Python 3.14+
**Project Type**: Single project (CLI application)  
**Performance Goals**: Add task <100ms, list tasks <200ms for typical usage (up to 1000 tasks)  
**Constraints**: Single-user local file access, no network dependencies, <50MB memory footprint  
**Scale/Scope**: MVP with 2 commands, ~500 LOC, extensible for future operations (delete, update, complete)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Code Quality First ✅ PASS
- **Single Responsibility**: Each module (CLI, Storage, Models) has one clear purpose
- **Clear Naming**: `TaskStorage`, `add_task()`, `list_tasks()` - self-documenting names
- **DRY Principle**: Shared logic centralized in storage module
- **Static Analysis**: Will use ruff for linting, mypy for type checking, black for formatting
- **Documentation**: All public functions will have docstrings with examples

### Principle II: Comprehensive Testing Standards ✅ PASS
- **Test-First Development**: Tests written before implementation (per TDD cycle)
- **Red-Green-Refactor**: Workflow will follow strict TDD
- **Test Coverage Minimum**: Target 80%+ coverage (pytest-cov)
- **Test Types**:
  - Unit tests for storage operations, task model, CLI parsing
  - Integration tests for end-to-end command flows
  - Contract tests for storage interface
- **Test Quality**: Fast (<5s total), deterministic, independent
- **Continuous Testing**: Tests run via uv run pytest

### Principle III: User Experience Consistency ✅ PASS
- **Interaction Patterns**: Consistent command structure (`tasks <subcommand> [args]`)
- **Error Handling UX**: Clear, actionable error messages (e.g., "Task description cannot be empty")
- **User Feedback**: Immediate confirmation messages for add, clear output for list
- **Consistent Tone**: Friendly, helpful error messages

### Principle IV: Performance Requirements ✅ PASS
- **Runtime Performance**: CLI responds <100ms for add, <200ms for list (meets <100ms requirement)
- **Memory**: Minimal footprint (<50MB), no memory leaks (JSON loaded/written per operation)
- **Scalability**: Handles 1000+ tasks without degradation

### Principle V: User Documentation ✅ PASS
- **Documentation Required**: README.md with installation, usage examples, troubleshooting
- **Up-to-Date**: Documentation created alongside implementation
- **Types**: User guide (quickstart.md), API docs (module docstrings), troubleshooting section

### Principle VI: Use Emojis in Output ⚠️ DISCRETIONARY
- Not applicable for CLI tool output (would interfere with parsing/scripting)
- Will use emojis in documentation and commit messages instead

**Overall Status**: ✅ ALL CRITICAL GATES PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── tasks_cli/
│   ├── __init__.py
│   ├── __main__.py          # Entry point for `python -m tasks_cli` and `tasks` command
│   ├── cli.py               # CLI argument parsing and command routing
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── add.py           # Add command implementation
│   │   └── list.py          # List command implementation
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task dataclass/model
│   └── storage/
│       ├── __init__.py
│       └── task_storage.py  # JSON file storage operations

tests/
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py
│   ├── test_task_storage.py
│   ├── test_add_command.py
│   └── test_list_command.py
├── integration/
│   ├── __init__.py
│   └── test_cli_end_to_end.py
└── contract/
    ├── __init__.py
    └── test_storage_contract.py

pyproject.toml               # uv project configuration
README.md                    # User documentation
.python-version              # Python version specification (3.14)
```

**Structure Decision**: Using Option 1 (Single project) with Python package structure. The `src/` layout follows Python best practices with the package name `tasks_cli` to avoid conflicts with the command name `tasks`. Tests are organized by type (unit, integration, contract) as per constitution testing requirements. The CLI and storage components are clearly separated into distinct modules under `cli.py` and `storage/`, satisfying FR-007's logical separation requirement.

## Complexity Tracking

> **No violations to justify** - All constitution principles satisfied without requiring exceptions.

---

# Phase 0: Research & Technology Decisions

## Research Questions

Based on Technical Context unknowns, we need to clarify:

1. ✅ **uv project initialization**: Best practices for Python 3.14 project setup with uv
2. ✅ **CLI framework choice**: argparse (stdlib) vs typer vs click
3. ✅ **Path handling**: Best practices for cross-platform home directory resolution
4. ✅ **JSON storage patterns**: Atomic writes, corruption handling, schema evolution
5. ✅ **Entry point configuration**: Console scripts via uv/setuptools
6. ✅ **Testing strategy**: pytest configuration, mocking file operations, test fixtures

## Research Findings

### 1. uv Project Initialization
**Decision**: Use uv for full project lifecycle
- **Rationale**: uv is a modern, fast Python package manager that handles project initialization, dependency management, and script execution
- **Pattern**: `uv init --lib tasks-cli` creates project structure, `uv add` manages dependencies, `uv run` executes scripts
- **Benefits**: Faster than pip, lockfile support, built-in virtual environment management

### 2. CLI Framework Choice
**Decision**: Use argparse (standard library)
- **Rationale**: Minimal dependencies align with constitution principle of simplicity; sufficient for 2 commands
- **Alternatives Considered**:
  - **Typer**: Rich features but adds dependency; overkill for MVP
  - **Click**: Popular but adds dependency; unnecessary for simple command structure
- **Pattern**: `ArgumentParser` with subparsers for `add` and `list` commands

### 3. Path Handling
**Decision**: Use `pathlib.Path.home()` for cross-platform home directory
- **Rationale**: Standard library, handles Windows/macOS/Linux automatically
- **Pattern**: `Path.home() / ".tasks.json"` resolves to correct home on all platforms
- **Fallback**: Environment variable override via `TASKS_FILE` for testing/customization

### 4. JSON Storage Patterns
**Decision**: Atomic writes with tempfile + rename, corruption recovery
- **Rationale**: Prevents data loss on write failures, handles corrupted files gracefully
- **Pattern**:
  - Read: `json.load()` with try/except for corruption handling
  - Write: Write to temp file → rename (atomic on POSIX, near-atomic on Windows)
  - Schema: Array of task objects `[{"id": 1, "description": "...", "timestamp": "...", "status": "pending"}]`
- **Corruption Handling**: Catch `JSONDecodeError`, log error, prompt user for recovery (backup old file, start fresh)

### 5. Entry Point Configuration  
**Decision**: Configure console script in `pyproject.toml`
- **Rationale**: uv supports PEP 621 project metadata with console scripts
- **Pattern**:
  ```toml
  [project.scripts]
  tasks = "tasks_cli.__main__:main"
  ```
- **Execution**: Users can run `tasks add "..."` after installation

### 6. Testing Strategy
**Decision**: pytest with fixtures for file mocking, tmp_path for integration tests
- **Rationale**: pytest is industry standard, excellent fixture support, clean syntax
- **Pattern**:
  - **Unit tests**: Mock file I/O with `unittest.mock.mock_open` or in-memory storage
  - **Integration tests**: Use pytest's `tmp_path` fixture for real file operations
  - **Contract tests**: Verify storage interface without implementation details
- **Coverage**: pytest-cov plugin for coverage reporting (target 80%+)

## Technology Stack Summary

| Layer | Technology | Justification |
|-------|------------|---------------|
| Language | Python 3.14+ | Modern features, excellent stdlib, wide adoption |
| Package Manager | uv | Fast, modern, lockfile support, built-in venv |
| CLI Framework | argparse | Stdlib, zero dependencies, sufficient for needs |
| Storage Format | JSON | Human-readable, stdlib support, debugging-friendly |
| Testing | pytest + pytest-cov | Industry standard, great fixtures, coverage reporting |
| Linting | ruff | Fast, comprehensive, replaces multiple tools |
| Type Checking | mypy | Static type analysis, catches bugs early |
| Formatting | black | Opinionated, consistent, low configuration |

---

# Phase 1: Design & Contracts

## Data Model

### Task Entity

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
        timestamp: ISO 8601 timestamp when task was created
        status: Current status (only 'pending' in MVP, extensible)
    """
    id: int
    description: str
    timestamp: str  # ISO 8601 format
    status: Literal["pending"] = "pending"
    
    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            "id": self.id,
            "description": self.description,
            "timestamp": self.timestamp,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize from dictionary."""
        return cls(
            id=data["id"],
            description=data["description"],
            timestamp=data["timestamp"],
            status=data.get("status", "pending")
        )
```

### Storage Schema

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
  }
]
```

**Schema Evolution**: Version field can be added later for migrations. Current schema is v1 (implicit).

## API Contracts

### Storage Interface

```python
from pathlib import Path
from typing import List, Optional
from tasks_cli.models.task import Task

class TaskStorage:
    """Handles persistent storage of tasks in JSON format.
    
    This class is completely agnostic to how it's called (CLI, API, tests).
    It provides a clean interface for CRUD operations on tasks.
    """
    
    def __init__(self, file_path: Optional[Path] = None):
        """Initialize storage with file path.
        
        Args:
            file_path: Path to JSON storage file. Defaults to ~/.tasks.json
        """
        self.file_path = file_path or Path.home() / ".tasks.json"
    
    def add_task(self, description: str) -> Task:
        """Add a new task to storage.
        
        Args:
            description: Task description (1-1000 characters)
            
        Returns:
            Created Task object with assigned ID and timestamp
            
        Raises:
            ValueError: If description is empty or too long
            IOError: If file cannot be written
        """
        ...
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from storage.
        
        Returns:
            List of Task objects, empty list if no tasks exist
            
        Raises:
            IOError: If file cannot be read
            ValueError: If JSON is corrupted
        """
        ...
    
    def _read_tasks(self) -> List[Task]:
        """Internal: Read tasks from file."""
        ...
    
    def _write_tasks(self, tasks: List[Task]) -> None:
        """Internal: Write tasks to file atomically."""
        ...
    
    def _get_next_id(self, tasks: List[Task]) -> int:
        """Internal: Calculate next sequential ID."""
        ...
```

### CLI Interface

```python
import sys
from tasks_cli.commands.add import add_command
from tasks_cli.commands.list import list_command

def main() -> int:
    """Main entry point for tasks CLI.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        prog="tasks",
        description="Command-line task management"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Add subcommand
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    
    # List subcommand
    list_parser = subparsers.add_parser("list", help="List all tasks")
    
    args = parser.parse_args()
    
    try:
        if args.command == "add":
            return add_command(args.description)
        elif args.command == "list":
            return list_command()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0
```

## Quickstart Documentation

See [quickstart.md](./quickstart.md) for user-facing installation and usage guide.

---

# Post-Phase 1 Constitution Re-check

### Principle I: Code Quality First ✅ PASS
- Clear module boundaries: models, storage, CLI, commands
- Self-documenting names maintained in contracts
- No code duplication in design

### Principle II: Comprehensive Testing Standards ✅ PASS
- Contract tests verify storage interface
- Unit tests for each module identified
- Integration tests for CLI end-to-end flows
- All testable without implementation

### Principle III: User Experience Consistency ✅ PASS
- Consistent command structure in CLI design
- Clear error messages specified in contracts
- Simple, predictable interface

### Principle IV: Performance Requirements ✅ PASS
- Design supports <100ms operations (in-memory sorting, direct file I/O)
- No performance bottlenecks in architecture

### Principle V: User Documentation ✅ PASS
- quickstart.md created with usage examples
- API contracts document all public methods
- README will include installation, examples, troubleshooting

**Overall Status**: ✅ ALL GATES PASSED - Ready for Phase 2 (Tasks)
