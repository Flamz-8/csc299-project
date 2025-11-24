# Implementation Plan: Pro Study Planner

**Branch**: `001-student-pkm-cli` | **Date**: 2025-11-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-student-pkm-cli/spec.md`

## Summary

Build a terminal-based personal knowledge management app for students that combines note-taking and task management in a single CLI tool. The system prioritizes "quick capture" workflow with minimal friction, allowing students to rapidly save notes/tasks to an inbox and organize them later by course and topic. Core value: reduce cognitive load by keeping all academic information in one fast, offline, keyboard-driven tool that answers "what should I work on next?"

**Technical Approach**: Python 3.11+ CLI application initialized with `uv`, using Click for command parsing, JSON for human-readable local storage, and rich/colorama for terminal UI. Architecture follows single-project structure with clear separation: models (data entities), services (business logic), cli (command handlers), and storage (JSON persistence). Test-first development with pytest, aiming for <1s startup and <500ms for all view operations.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Click (CLI framework), python-dateutil (date parsing), rich (terminal formatting), pydantic (data validation)  
**Storage**: JSON files (local filesystem, human-readable)  
**Testing**: pytest (unit/integration), pytest-cov (coverage), hypothesis (property-based for edge cases)  
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows via Python runtime)
**Project Type**: single (standalone CLI application)  
**Package Manager**: uv (fast Python package installer and resolver)  
**Performance Goals**: <1s app launch, <500ms filtered views (500 tasks), <1s search (1000 notes + 500 tasks), <5s single command capture  
**Constraints**: No network calls, <100MB memory for typical datasets, cross-platform path handling, atomic file writes for data safety  
**Scale/Scope**: 10-20 courses/semester, 50-200 notes, 20-100 active tasks per student

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Validate this feature against constitution principles (`.specify/memory/constitution.md`):

**I. Code Quality First**:
- [x] Linting/formatting tools configured for this feature's tech stack (ruff for linting, black/ruff format for formatting, mypy for type checking)
- [x] Code complexity limits defined (cyclomatic complexity ≤10, enforced by ruff)
- [x] Public API documentation requirements understood (all CLI commands, models, and services documented with docstrings)
- [x] Type safety approach determined (strict typing with Python 3.11+ type hints, mypy --strict mode, pydantic for runtime validation)
- [x] User documentation planned (README with installation, quickstart.md with examples, inline help system)

**II. Testing Standards**:
- [x] Test-first workflow planned (tests before implementation for all user stories)
- [x] Test categories identified: Unit (models, services, utilities), Integration (CLI commands end-to-end), Contract (JSON schema validation), Edge Cases (invalid inputs, corrupted data)
- [x] Coverage targets defined (≥80% line coverage, 100% for data persistence and critical paths like file I/O)
- [x] Test independence verified (pytest fixtures for isolated test data, no shared state between tests)

**III. User Experience Consistency**:
- [x] Response time budgets defined (<100ms command acknowledgment, <1s p95 for all operations, <500ms for filtered views)
- [x] Error message standards established (human-readable with actionable guidance, consistent format: "Error: [problem]. Try: [solution]", no stack traces unless --debug)
- [x] Accessibility requirements identified (terminal-based = screen reader compatible, keyboard-only navigation, high-contrast color schemes via rich library)
- [x] Design system components identified (rich tables for lists, colored status indicators, consistent formatting for IDs/timestamps)
- [x] Loading states and offline behavior planned (spinners for >200ms operations, graceful handling of missing files, atomic writes to prevent corruption)

**IV. Performance Requirements**:
- [x] Performance budgets defined (p50: 50ms, p95: 500ms for views; p99: 1s for search; memory: <50MB for 200 notes + 100 tasks)
- [x] Performance testing approach planned (pytest-benchmark for critical paths, manual testing with 500 tasks dataset, profiling with cProfile if needed)
- [x] Monitoring strategy defined (no runtime monitoring for CLI, but performance tests in CI, timing logs for operations >100ms in --debug mode)
- [x] Database performance considerations (N/A - file-based storage; use efficient JSON loading, lazy loading for large datasets if needed)

**Violations Requiring Justification**: None


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
student-pkm-cli/
├── pyproject.toml           # uv project configuration, dependencies
├── README.md                # Installation and overview
├── .python-version          # Python version (3.11)
├── uv.lock                  # Locked dependencies
├── .gitignore
├── src/
│   └── pkm/
│       ├── __init__.py
│       ├── __main__.py      # Entry point: python -m pkm
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py      # Click application root
│       │   ├── add.py       # add command group
│       │   ├── view.py      # view command group
│       │   ├── organize.py  # organize command group
│       │   ├── task.py      # task command group
│       │   ├── search.py    # search command
│       │   └── helpers.py   # CLI utilities (formatting, prompts)
│       ├── models/
│       │   ├── __init__.py
│       │   ├── note.py      # Note model (pydantic)
│       │   ├── task.py      # Task model (pydantic)
│       │   ├── course.py    # Course model (pydantic)
│       │   └── common.py    # Shared types (ID, timestamps)
│       ├── services/
│       │   ├── __init__.py
│       │   ├── note_service.py    # Note business logic
│       │   ├── task_service.py    # Task business logic
│       │   ├── search_service.py  # Search logic
│       │   └── id_generator.py    # Unique ID generation
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── json_store.py      # JSON file I/O
│       │   ├── schema.py          # Data schema definitions
│       │   └── migrations.py      # Data migration utilities
│       └── utils/
│           ├── __init__.py
│           ├── date_parser.py     # Natural language date parsing
│           ├── editor.py          # External editor integration
│           └── config.py          # Configuration management
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   ├── test_storage.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── test_add_commands.py
│   │   ├── test_view_commands.py
│   │   ├── test_organize_commands.py
│   │   ├── test_task_commands.py
│   │   └── test_search_commands.py
│   ├── contract/
│   │   └── test_json_schema.py
│   └── edge_cases/
│       ├── test_corrupted_data.py
│       ├── test_invalid_dates.py
│       └── test_missing_files.py
└── docs/
    └── (quickstart.md will be generated here)
```

**Structure Decision**: Single project layout selected because this is a standalone CLI application with no backend/frontend separation. All code resides in `src/pkm/` following Python package conventions. Tests mirror source structure for easy navigation. Using `src/` layout (PEP 420) to avoid accidental imports from development directory.

## Complexity Tracking

> **No violations** - Constitution Check passed. All principles satisfied with straightforward Python CLI architecture.

---

## Artifacts Generated

### Phase 0: Research (COMPLETE)

✅ **research.md**
- 10 technical decisions documented
- Python 3.11+ with uv package manager
- Click CLI framework + Pydantic models + rich formatting
- JSON storage with atomic writes
- Full test strategy (pytest, 4 test categories)
- Performance optimization strategies

### Phase 1: Design & Contracts (COMPLETE)

✅ **data-model.md**
- 6 entities defined: Note, Task, Subtask, Course, Topic, Inbox (virtual)
- Pydantic schemas with validation rules
- Entity relationships and computed fields
- ID generation strategy (type_timestamp_random)
- JSON storage schema with migration strategy
- Data integrity rules and indexes for performance

✅ **contracts/cli-interface.md**
- 15 core commands across 6 command groups
- Global options (--data-dir, --no-color, --verbose)
- Input/output contracts with examples
- Error handling patterns with exit codes
- Rich formatting specification
- Performance targets per Constitution Check

✅ **quickstart.md**
- Installation guide (uv, Python 3.11+)
- First steps (capture → organize → view)
- 5 common workflows with examples
- Top 5 commands reference
- Sample data walkthrough (Monday-Friday)
- Troubleshooting guide

✅ **Agent Context Updated**
- GitHub Copilot instructions file created
- Python 3.11+, Click, Pydantic, rich, JSON storage added
- Feature-specific patterns documented

### Phase 2: Task Breakdown (PENDING)

⏳ **tasks.md** - NOT created by /speckit.plan
- Run `/speckit.tasks` to generate implementation task breakdown
- Tasks organized by user story priority (P1 → P2 → P3)
- Each task linked to specific requirements and success criteria

---

## Next Steps

### 1. Re-evaluate Constitution Check (Post-Design)

All principles remain satisfied after Phase 1 design:

- ✅ **Code Quality**: Pydantic models enforce type safety, rich provides consistent output formatting
- ✅ **Testing**: 4 test categories defined (unit, integration, contract, edge cases)
- ✅ **UX Consistency**: <1s performance targets defined for all commands, rich library ensures uniform formatting
- ✅ **Performance**: Indexes planned for <500ms filtered views, atomic writes for data integrity

**No new violations introduced by design decisions.**

### 2. Command Completion

**Branch**: `001-student-pkm-cli`  
**Plan Location**: `specs/001-student-pkm-cli/plan.md`

**Generated Artifacts**:
- `specs/001-student-pkm-cli/research.md` (Phase 0)
- `specs/001-student-pkm-cli/data-model.md` (Phase 1)
- `specs/001-student-pkm-cli/contracts/cli-interface.md` (Phase 1)
- `specs/001-student-pkm-cli/quickstart.md` (Phase 1)
- `.github/agents/copilot-instructions.md` (Agent context)

**Recommended Next Command**:
```bash
# Generate implementation task breakdown
/speckit.tasks
```

This will create `specs/001-student-pkm-cli/tasks.md` with actionable implementation steps organized by user story priority.
