# Research: Task Management CLI

**Feature**: Task Management CLI  
**Date**: 2025-11-19  
**Phase**: Phase 0 - Technology Research

## Overview

This document captures research findings for implementing a Python-based task management CLI application using modern tooling (uv, Python 3.14+) with emphasis on simplicity, testability, and separation of concerns.

## Research Areas

### 1. uv Project Initialization & Management

**Question**: What are the best practices for setting up a Python 3.14 project with uv?

**Findings**:
- **uv** is a modern Python package manager written in Rust, significantly faster than pip
- Supports PEP 621 `pyproject.toml` standard for project metadata
- Built-in virtual environment management (no need for separate venv commands)
- Lockfile support (`uv.lock`) for reproducible builds

**Best Practices**:
```bash
# Initialize new project
uv init --app tasks-cli

# Add dependencies
uv add pytest pytest-cov

# Add dev dependencies  
uv add --dev ruff mypy black

# Run commands in project environment
uv run pytest
uv run tasks add "Buy groceries"

# Install project in development mode
uv pip install -e .
```

**Decision**: Use uv for full project lifecycle
- **Rationale**: Modern, fast, handles initialization, dependencies, and execution
- **Benefits**: Single tool for all package management needs, faster installs, lockfile support

**References**:
- uv documentation: https://github.com/astral-sh/uv
- PEP 621: https://peps.python.org/pep-0621/

---

### 2. CLI Framework Selection

**Question**: Which CLI framework best fits our needs (argparse, typer, click)?

**Comparison**:

| Framework | Pros | Cons | Dependencies |
|-----------|------|------|--------------|
| argparse | Stdlib, zero deps, sufficient for simple CLIs | Verbose for complex CLIs | None |
| typer | Type hints, auto-completion, rich features | Adds dependency (click + rich) | click, rich, typing-extensions |
| click | Popular, decorator-based, good docs | Adds dependency | None (but external) |

**Requirements Analysis**:
- MVP needs: 2 commands (add, list) with minimal arguments
- No complex validation, nested commands, or interactive features
- Constitution principle: minimize dependencies

**Decision**: Use argparse (standard library)
- **Rationale**: Two simple commands don't justify external dependencies; argparse is sufficient
- **Pattern**: ArgumentParser with subparsers for command routing
- **Future**: Can migrate to typer if command complexity grows (delete, update, search with filters)

**Example Structure**:
```python
import argparse

parser = argparse.ArgumentParser(prog="tasks")
subparsers = parser.add_subparsers(dest="command", required=True)

# Add command
add_parser = subparsers.add_parser("add")
add_parser.add_argument("description")

# List command
list_parser = subparsers.add_parser("list")

args = parser.parse_args()
```

---

### 3. Cross-Platform Path Handling

**Question**: How to reliably locate home directory across Windows, macOS, Linux?

**Findings**:
- **pathlib.Path.home()** (Python 3.4+): Cross-platform home directory resolution
- Handles platform differences automatically:
  - Windows: `C:\Users\username`
  - macOS: `/Users/username`
  - Linux: `/home/username`
- Returns `Path` object for modern path operations

**Best Practices**:
```python
from pathlib import Path
import os

# Recommended: pathlib for cross-platform support
storage_path = Path.home() / ".tasks.json"

# Alternative: Environment variable override for testing/customization
storage_path = Path(os.getenv("TASKS_FILE", Path.home() / ".tasks.json"))
```

**Decision**: Use `pathlib.Path.home()` with environment variable override
- **Rationale**: Standard library, platform-agnostic, modern API
- **Testing**: `TASKS_FILE` env var allows test isolation
- **Pattern**: Default to home directory, allow override for advanced users

---

### 4. JSON Storage & Atomic Writes

**Question**: How to safely write JSON files to prevent corruption and data loss?

**Findings**:

**Corruption Scenarios**:
1. Program crash during write
2. Disk full during write
3. Manual file editing introduces syntax errors
4. Power failure during write

**Atomic Write Pattern**:
```python
import json
import tempfile
from pathlib import Path

def atomic_write_json(data, file_path: Path):
    """Write JSON atomically using temp file + rename."""
    # Write to temporary file in same directory
    temp_fd, temp_path = tempfile.mkstemp(
        dir=file_path.parent,
        suffix=".tmp"
    )
    
    try:
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename (POSIX) / near-atomic (Windows)
        os.replace(temp_path, file_path)
    except:
        # Clean up temp file on failure
        Path(temp_path).unlink(missing_ok=True)
        raise
```

**Corruption Recovery**:
```python
def read_tasks_with_recovery(file_path: Path):
    """Read tasks with corruption handling."""
    try:
        with open(file_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        # Backup corrupted file
        backup_path = file_path.with_suffix(".json.backup")
        shutil.copy(file_path, backup_path)
        
        print(f"Error: Tasks file is corrupted. Backed up to {backup_path}")
        print("Starting with empty task list.")
        return []
    except FileNotFoundError:
        # File doesn't exist yet - normal for first run
        return []
```

**Decision**: Implement atomic writes and corruption recovery
- **Rationale**: Prevents data loss, handles edge cases gracefully
- **Pattern**: Write to temp → rename for atomicity, backup + recover on corruption
- **User Experience**: Clear error messages, automatic recovery when possible

---

### 5. Entry Point & Console Scripts

**Question**: How to make `tasks` command available after installation?

**Findings**:

**PEP 621 Console Scripts**:
```toml
# pyproject.toml
[project]
name = "tasks-cli"
version = "0.1.0"

[project.scripts]
tasks = "tasks_cli.__main__:main"
```

**Entry Point Structure**:
```python
# src/tasks_cli/__main__.py
def main():
    """Entry point for tasks CLI."""
    import sys
    from tasks_cli.cli import run_cli
    sys.exit(run_cli())

if __name__ == "__main__":
    main()
```

**Installation Methods**:
```bash
# Development installation (editable)
uv pip install -e .

# After this, `tasks` command is available globally

# Or run directly without installation
uv run python -m tasks_cli add "Test task"
```

**Decision**: Configure console script in pyproject.toml
- **Rationale**: Standard Python packaging approach, uv compatible
- **Pattern**: `tasks` → `tasks_cli.__main__:main` entry point
- **Development**: Use `uv run` for testing before installation

---

### 6. Testing Strategy & pytest Configuration

**Question**: How to structure tests for CLI application with file I/O?

**Testing Pyramid**:
```
        E2E (Integration)
       /                \
      /    Contract      \
     /                    \
    /        Unit          \
   /__________________________\
```

**Test Types**:

1. **Unit Tests** (Fast, isolated):
   - Task model serialization/deserialization
   - ID generation logic
   - String validation (empty, too long)
   - Sorting logic (case-insensitive alphabetical)

2. **Contract Tests** (Interface verification):
   - Storage interface methods exist
   - Correct signatures and return types
   - Error handling contracts

3. **Integration Tests** (End-to-end):
   - CLI commands with real file I/O (using temp directories)
   - Add task → verify in file → list tasks
   - Error scenarios (corrupted file, permissions)

**pytest Configuration**:
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=tasks_cli",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
    "-v"
]
```

**Fixture Patterns**:
```python
import pytest
from pathlib import Path

@pytest.fixture
def temp_storage(tmp_path):
    """Provide temporary storage path for tests."""
    return tmp_path / "test_tasks.json"

@pytest.fixture
def storage_with_tasks(temp_storage):
    """Provide storage pre-populated with test tasks."""
    from tasks_cli.storage import TaskStorage
    storage = TaskStorage(temp_storage)
    storage.add_task("Task 1")
    storage.add_task("Task 2")
    return storage
```

**Decision**: pytest with three-tier testing strategy
- **Rationale**: Comprehensive coverage, fast feedback, good isolation
- **Pattern**: Unit tests for logic, contract tests for interfaces, integration for E2E
- **Coverage**: Target 80%+ with pytest-cov

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| Language | Python | 3.14+ | Modern features, excellent stdlib, type hints |
| Package Manager | uv | latest | Fast, modern, lockfile support |
| CLI Framework | argparse | stdlib | Zero dependencies, sufficient for needs |
| Storage Format | JSON | stdlib | Human-readable, stdlib support |
| Testing | pytest | 8.x | Industry standard, great fixtures |
| Coverage | pytest-cov | 5.x | Coverage reporting and enforcement |
| Linting | ruff | latest | Fast, comprehensive, replaces flake8/isort |
| Type Checking | mypy | 1.x | Static analysis, catches bugs early |
| Formatting | black | latest | Consistent, opinionated formatting |

## Alternatives Considered

### Why not Click/Typer?
- **Reason**: MVP has only 2 simple commands; argparse is sufficient
- **When to reconsider**: If commands grow to 5+ with complex arguments/validation

### Why not YAML/TOML for storage?
- **Reason**: JSON is simpler, has stdlib support, sufficient for task data
- **When to reconsider**: If users request human-editable format or comments

### Why not SQLite for storage?
- **Reason**: Overkill for MVP; JSON is simpler and more debuggable
- **When to reconsider**: If task count grows to 10,000+ or need complex queries

### Why not Poetry instead of uv?
- **Reason**: uv is significantly faster and handles same use cases
- **When to reconsider**: If team already standardized on Poetry

## Open Questions & Future Research

### Resolved in This Phase
- ✅ uv project setup
- ✅ CLI framework choice
- ✅ Path handling
- ✅ JSON storage patterns
- ✅ Entry point configuration
- ✅ Testing strategy

### Deferred to Implementation
- Command-line argument edge cases (special characters, very long descriptions)
- Exact error message wording (will be refined during implementation)
- Performance profiling (will measure after implementation)

### Future Enhancements (Out of MVP Scope)
- Task completion/status updates
- Task deletion and editing
- Search/filter functionality
- Configuration file support
- Shell completion (bash, zsh, fish)
- Task import/export (CSV, other formats)

## Conclusion

All research questions resolved. Technology stack selected based on:
- ✅ Simplicity (constitution principle)
- ✅ Minimal dependencies
- ✅ Cross-platform compatibility
- ✅ Testability
- ✅ Performance
- ✅ Maintainability

**Status**: Ready to proceed to Phase 1 (Design & Contracts)
