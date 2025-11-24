# Research: Pro Study Planner

**Phase**: 0 - Technology Research & Decision Rationale  
**Date**: 2025-11-23  
**For**: Implementation Plan `plan.md`

## Overview

This document captures research findings and technical decisions for building the Pro Study Planner. Each decision documents the rationale, alternatives considered, and how it aligns with constitution principles and success criteria.

---

## Decision 1: Python 3.11+ as Implementation Language

**Rationale**:
- **Cross-platform**: Python runs identically on Linux, macOS, Windows (meets FR-002)
- **Rich ecosystem**: Excellent CLI libraries (Click), date parsing (python-dateutil), terminal formatting (rich)
- **Type safety**: Python 3.11+ has strong type hints + mypy for static analysis (constitution principle I)
- **Student-friendly**: Most students already have Python installed or can easily get it
- **Performance**: Fast enough for target workload (<1s startup, <500ms views with proper implementation)
- **JSON native**: Built-in json module for human-readable storage (FR-015)

**Alternatives Considered**:
- **Node.js**: Similar benefits, but Python more common in academic environments; JS async model overkill for file-based CLI
- **Rust**: Would exceed performance targets but harder learning curve for contributors, longer dev time
- **Go**: Good performance, but less rich CLI ecosystem; compiled binary nice but not essential for student tool

**Constitution Alignment**:
- ✅ Code Quality: mypy --strict enforces type safety
- ✅ Testing: pytest is industry-standard with excellent tooling
- ✅ UX: rich library provides consistent terminal formatting
- ✅ Performance: Meets all budgets with proper architecture

---

## Decision 2: uv for Package Management

**Rationale**:
- **Speed**: 10-100x faster than pip for installs/resolves (improves student onboarding experience)
- **Modern**: Rust-based tool with excellent dependency resolution
- **Simplicity**: Single `uv init` creates pyproject.toml + virtual env + lock file
- **Standard**: Uses PEP 621 pyproject.toml (not proprietary format)
- **Minimal setup**: Students run `uv sync` and they're ready (FR-002 minimal setup)

**Alternatives Considered**:
- **pip + venv**: Standard but slower, manual venv management, no lock file by default
- **Poetry**: Feature-rich but slower than uv, additional tool to learn
- **pipenv**: Falling out of favor, slower resolves

**Decision**: Use uv for initialization and dependency management, but fallback docs for pip users

---

## Decision 3: Click for CLI Framework

**Rationale**:
- **Composable commands**: Natural fit for `add`, `view`, `organize`, `task`, `search` command groups
- **Automatic help**: Generates help text from docstrings (FR-017, FR-018)
- **Parameter validation**: Built-in type checking for --due dates, --priority enums, etc.
- **Testable**: Commands are pure functions, easy to unit test
- **Pythonic**: Decorator-based, idiomatic Python code

**Alternatives Considered**:
- **argparse**: Standard library but verbose, manual help formatting
- **Typer**: Built on Click, adds type hints but less mature
- **Fire**: Too magical, harder to test, less control over UX

**Example**:
```python
@click.group()
def add():
    """Add notes or tasks to your PKM system."""
    pass

@add.command()
@click.argument('content')
@click.option('--course', help='Assign to course')
@click.option('--topic', help='Tag with topic')
def note(content, course, topic):
    """Add a new note."""
    # Implementation
```

---

## Decision 4: Pydantic for Data Models

**Rationale**:
- **Runtime validation**: Ensures JSON data matches schema (prevents corrupted data, FR-024)
- **Type safety**: Integrates with mypy for compile-time + runtime validation
- **Serialization**: Built-in JSON export/import with proper type handling
- **Documentation**: Models serve as schema documentation
- **Default values**: Easy to define defaults (e.g., priority='medium', status=False)

**Alternatives Considered**:
- **dataclasses**: Standard library but no runtime validation
- **attrs**: Similar to dataclasses, less integration with JSON serialization
- **Manual dicts**: Error-prone, no type safety

**Example**:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Note(BaseModel):
    id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    course: Optional[str] = None
    topics: list[str] = Field(default_factory=list)
```

---

## Decision 5: rich for Terminal Formatting

**Rationale**:
- **Consistent UX**: Tables, colors, progress indicators (constitution principle III)
- **Accessibility**: Respects NO_COLOR env var, high-contrast themes
- **Cross-platform**: Handles Windows/Unix terminal differences
- **Performance**: Fast rendering, no noticeable latency
- **Modern**: Beautiful output improves student engagement

**Alternatives Considered**:
- **colorama**: Only colors, no tables/formatting
- **termcolor**: Similar limitations to colorama
- **Plain text**: Works but less engaging for students

**Features Used**:
- Tables for `view inbox`, `list courses`
- Colored status (green=complete, yellow=due today, red=overdue)
- Spinners for operations >200ms
- Syntax highlighting for search results

---

## Decision 6: JSON File Storage with Atomic Writes

**Rationale**:
- **Human-readable**: Students can inspect/backup with text editor (FR-015, SC-007)
- **No database**: Meets "zero external dependencies" (FR-016)
- **Simple**: No schema migrations, no query language to learn
- **Cross-platform**: Works everywhere Python works
- **Atomic writes**: Write to temp file + rename prevents corruption (FR-024)

**Architecture**:
```
~/.pkm/
├── data.json          # Main data file
├── data.json.bak      # Automatic backup
└── config.json        # User preferences
```

**Data Structure**:
```json
{
  "version": "1.0.0",
  "notes": [...],
  "tasks": [...],
  "courses": [...],
  "last_modified": "2025-11-23T10:30:00Z"
}
```

**Alternatives Considered**:
- **SQLite**: Overkill for this scale, not human-editable
- **Multiple JSON files**: More complex, harder atomic updates
- **TOML/YAML**: Less standard for data storage, Python libs slower

---

## Decision 7: python-dateutil for Date Parsing

**Rationale**:
- **Natural language**: Handles "tomorrow", "next friday", "12/15" (spec notes)
- **Timezone aware**: Proper handling of local time
- **Robust**: Industry-standard library, well-tested
- **Flexible**: Supports multiple date formats automatically

**Alternatives Considered**:
- **Manual parsing**: Error-prone, poor UX
- **dateparser**: More features but heavier dependency
- **Arrow**: Similar to dateutil but less standard

**Example**:
```python
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

# Handles: "2025-11-25", "tomorrow", "next week"
due_date = parse(user_input, fuzzy=True)
```

---

## Decision 8: Test Strategy

**Test Categories** (constitution principle II):

1. **Unit Tests** (tests/unit/)
   - Models: Validation, serialization, edge cases
   - Services: Business logic isolated from I/O
   - Utils: Date parsing, ID generation, editor integration

2. **Integration Tests** (tests/integration/)
   - CLI commands end-to-end using Click's testing utilities
   - Real JSON file I/O (with temp directories)
   - Full user workflows (add → organize → view)

3. **Contract Tests** (tests/contract/)
   - JSON schema validation
   - Backward compatibility for data format
   - Migration testing

4. **Edge Cases** (tests/edge_cases/)
   - Corrupted JSON recovery
   - Invalid date formats
   - Missing $EDITOR fallback
   - Concurrent access (file locking)

**Tools**:
- pytest: Test runner
- pytest-cov: Coverage reporting (target: 80%+)
- hypothesis: Property-based testing for edge cases
- pytest-mock: Mocking for external dependencies (subprocess for editor)

**Performance Tests**:
- Benchmark with pytest-benchmark for critical paths
- Test with realistic datasets: 200 notes, 100 tasks
- Verify <1s startup, <500ms views, <1s search

---

## Decision 9: Error Handling Strategy

**Constitution Principle III**: Human-readable, actionable error messages

**Error Categories**:

1. **User Errors** (4xx mental model):
   - Invalid commands → Suggest similar commands
   - Bad date formats → Show expected formats with examples
   - Missing IDs → List available IDs
   - Example: `Error: Note ID '999' not found. Try: pkm view inbox`

2. **System Errors** (5xx mental model):
   - Corrupted data → Automatic backup, offer recovery
   - Missing $EDITOR → Fall back to nano/vim/notepad by platform
   - File permissions → Clear message with fix instructions
   - Example: `Error: Cannot write to ~/.pkm/data.json (permission denied). Try: chmod 644 ~/.pkm/data.json`

3. **Edge Cases**:
   - Empty inbox → Friendly message suggesting quick start
   - No matches in search → Suggest checking spelling
   - File locked → Wait and retry with backoff

**Implementation**:
```python
class PKMError(Exception):
    """Base exception with user-friendly formatting."""
    def __init__(self, problem: str, solution: str):
        self.problem = problem
        self.solution = solution
        super().__init__(f"{problem}. Try: {solution}")
```

---

## Decision 10: Platform-Specific Considerations

**Cross-Platform Requirements** (FR-002):

1. **Path Handling**:
   - Use `pathlib.Path` for all file operations
   - Automatic handling of Windows/Unix separators
   - Home directory: `Path.home() / '.pkm'`

2. **Editor Detection**:
   - Priority: $EDITOR env var → platform default
   - Windows: notepad.exe
   - macOS: nano (bundled)
   - Linux: nano or vim

3. **Line Endings**:
   - JSON: Always write with `\n` (JSON spec)
   - Text editor: Let editor handle platform preference

4. **Terminal Colors**:
   - Detect NO_COLOR env var
   - Fallback to plain text if terminal doesn't support colors
   - rich library handles this automatically

---

## Performance Optimization Strategy

**Targets** (from Success Criteria):
- App launch: <1s (SC-002)
- Filtered views: <500ms for 500 tasks (SC-003)
- Search: <1s for 1000 notes + 500 tasks (SC-004)
- Capture: <5s (SC-001)

**Optimizations**:

1. **Lazy Loading**:
   - Don't load data.json until first command that needs it
   - Cache parsed JSON in memory for multi-command sessions (REPL mode)

2. **Efficient Filtering**:
   - Build indexes for common queries (by course, by due date)
   - Use generator expressions for large lists
   - Only load needed fields for list views

3. **Search Optimization**:
   - Simple string matching (no regex) for speed
   - Case-insensitive with str.lower() pre-processing
   - Limit results to top 50 by default

4. **Startup Optimization**:
   - Import Click lazily in subcommands
   - Defer rich imports until rendering needed
   - Use `if TYPE_CHECKING:` for type-only imports

**Benchmarks to Track**:
```python
def test_startup_time(benchmark):
    """App launch under 1 second."""
    result = benchmark(lambda: subprocess.run(['pkm', '--version']))
    assert benchmark.stats['mean'] < 1.0

def test_view_inbox_500_tasks(benchmark):
    """View inbox with 500 items under 500ms."""
    # Setup: create 500 tasks
    result = benchmark(lambda: subprocess.run(['pkm', 'view', 'inbox']))
    assert benchmark.stats['mean'] < 0.5
```

---

## Summary

**Key Technologies**:
- Python 3.11+ (type safety, cross-platform)
- uv (fast package management)
- Click (CLI framework)
- Pydantic (data validation)
- rich (terminal formatting)
- pytest (testing)

**Critical Patterns**:
- Atomic file writes for data safety
- Test-first development for all features
- Human-readable error messages
- Performance benchmarks in CI

**Risk Mitigation**:
- JSON corruption → Automatic backups + recovery
- Platform differences → pathlib + rich handle abstractions
- Performance → Lazy loading + benchmarks catch regressions
- Type errors → mypy --strict catches before runtime

All decisions align with constitution principles and support the success criteria defined in spec.md.
