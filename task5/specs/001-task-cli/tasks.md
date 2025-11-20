# Tasks: Task Management CLI

**Input**: Design documents from `/specs/001-task-cli/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL in this specification. They are included below but marked as optional - implement if TDD approach is desired.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **- [ ]**: Checkbox (markdown task format)
- **[ID]**: Sequential task number (T001, T002, etc.)
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)
- Include exact file paths in descriptions

## Path Conventions

Single project structure (from plan.md):
- Source code: `src/tasks_cli/`
- Tests: `tests/`
- Configuration: `pyproject.toml`, `.python-version`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize uv project with Python 3.14+ in repository root using `uv init --app tasks-cli`
- [X] T002 Create `.python-version` file with `3.14` specification
- [X] T003 Configure `pyproject.toml` with project metadata, dependencies (none for MVP), and console script entry point `tasks = "tasks_cli.__main__:main"`
- [X] T004 Add development dependencies: `uv add --dev pytest pytest-cov ruff mypy black`
- [X] T005 [P] Create directory structure: `src/tasks_cli/`, `src/tasks_cli/models/`, `src/tasks_cli/storage/`, `src/tasks_cli/commands/`
- [X] T006 [P] Create test directory structure: `tests/unit/`, `tests/integration/`, `tests/contract/`
- [X] T007 [P] Configure ruff in `pyproject.toml` with linting rules per constitution code quality standards
- [X] T008 [P] Configure mypy in `pyproject.toml` with strict type checking enabled
- [X] T009 [P] Configure pytest in `pyproject.toml` with coverage settings (minimum 80% target)
- [X] T010 [P] Create `.gitignore` with Python, uv, IDE, and OS-specific exclusions

**Checkpoint**: Project structure ready, development tools configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T011 [P] Create `src/tasks_cli/__init__.py` with package version metadata
- [X] T012 [P] Create Task model dataclass in `src/tasks_cli/models/task.py` with id, description, timestamp, status attributes and validation in `__post_init__`
- [X] T013 [P] Create `to_dict()` and `from_dict()` methods in Task model for JSON serialization
- [X] T014 Create TaskStorage class skeleton in `src/tasks_cli/storage/task_storage.py` with `__init__`, `add_task`, `get_all_tasks` method signatures
- [X] T015 Implement `_read_tasks()` private method in TaskStorage to read and parse JSON file with corruption handling
- [X] T016 Implement `_write_tasks()` private method in TaskStorage with atomic write pattern (temp file + rename)
- [X] T017 Implement `_get_next_id()` private method in TaskStorage to calculate sequential IDs
- [X] T018 [P] Create `src/tasks_cli/__main__.py` with main() entry point skeleton and argparse setup
- [X] T019 [P] Create `src/tasks_cli/cli.py` with ArgumentParser configuration for `tasks add` and `tasks list` subcommands

**Checkpoint**: Foundation ready - Task model complete, TaskStorage interface ready, CLI framework initialized

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks via `tasks add "description"` command with persistent storage

**Independent Test**: Run `tasks add "Buy groceries"` and verify task appears in ~/.tasks.json with ID, timestamp, and status

### Tests for User Story 1 (OPTIONAL - implement if TDD approach desired) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T020 [P] [US1] Unit test for Task model validation in `tests/unit/test_task_model.py` (empty description, long description, invalid ID)
- [ ] T021 [P] [US1] Unit test for Task serialization (`to_dict`, `from_dict`) in `tests/unit/test_task_model.py`
- [ ] T022 [P] [US1] Contract test for TaskStorage.add_task() in `tests/contract/test_storage_contract.py` using tmp_path fixture
- [ ] T023 [P] [US1] Integration test for `tasks add` command in `tests/integration/test_cli_end_to_end.py` with temporary storage file

### Implementation for User Story 1

- [X] T024 [US1] Implement TaskStorage.add_task() method in `src/tasks_cli/storage/task_storage.py`: validate description, generate ID, create timestamp, create Task object, append to storage, write atomically
- [X] T025 [US1] Create add command handler in `src/tasks_cli/commands/add.py` with function `add_command(description: str) -> int` that instantiates TaskStorage and calls add_task()
- [X] T026 [US1] Add error handling in `add_command()` for ValueError (empty/long description) and IOError (write failures) with user-friendly messages
- [X] T027 [US1] Wire add command to CLI in `src/tasks_cli/__main__.py` main() function to call add_command() when args.command == "add"
- [X] T028 [US1] Add success feedback message in `add_command()`: "Task added: [ID] description"
- [X] T029 [US1] Handle edge case: create ~/.tasks.json automatically if it doesn't exist (implement in _write_tasks)
- [X] T030 [US1] Handle edge case: validate description is non-empty after stripping whitespace

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add tasks and they persist correctly

---

## Phase 4: User Story 2 - List Tasks (Priority: P2)

**Goal**: Enable users to view all stored tasks via `tasks list` command with case-insensitive alphabetical sorting

**Independent Test**: Pre-populate ~/.tasks.json with tasks, run `tasks list`, verify all tasks displayed in alphabetical order (case-insensitive)

### Tests for User Story 2 (OPTIONAL - implement if TDD approach desired) ⚠️

- [ ] T031 [P] [US2] Contract test for TaskStorage.get_all_tasks() in `tests/contract/test_storage_contract.py` with various scenarios (empty, multiple tasks, corrupted file)
- [ ] T032 [P] [US2] Unit test for alphabetical sorting logic in `tests/unit/test_list_command.py` (case-insensitive: "apple", "Banana", "cherry")
- [ ] T033 [P] [US2] Integration test for `tasks list` command in `tests/integration/test_cli_end_to_end.py` with empty storage and populated storage

### Implementation for User Story 2

- [X] T034 [US2] Implement TaskStorage.get_all_tasks() method in `src/tasks_cli/storage/task_storage.py`: read from file, parse JSON, convert to Task objects, handle missing file gracefully (return empty list)
- [X] T035 [US2] Create list command handler in `src/tasks_cli/commands/list.py` with function `list_command() -> int` that instantiates TaskStorage and calls get_all_tasks()
- [X] T036 [US2] Implement case-insensitive alphabetical sorting in `list_command()`: sort tasks by `task.description.lower()`
- [X] T037 [US2] Format task output in `list_command()`: "[ID] description" for each task, one per line
- [X] T038 [US2] Handle empty task list in `list_command()`: display "No tasks found" message
- [X] T039 [US2] Wire list command to CLI in `src/tasks_cli/__main__.py` main() function to call list_command() when args.command == "list"
- [X] T040 [US2] Add error handling in `list_command()` for IOError (read failures) and ValueError (corrupted JSON) with user-friendly messages
- [X] T041 [US2] Handle edge case: corrupted JSON file - backup to ~/.tasks.json.backup and notify user

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - complete task management workflow functional

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and finalization

- [X] T042 [P] Create `README.md` at repository root with installation instructions from quickstart.md (uv installation, project setup)
- [X] T043 [P] Add usage examples to `README.md`: basic add/list commands, real-world scenarios from quickstart.md
- [X] T044 [P] Add troubleshooting section to `README.md`: file permissions, corrupted JSON, disk full errors
- [X] T045 [P] Add docstrings to all public functions and classes in `src/tasks_cli/` modules (per constitution documentation requirements)
- [X] T046 Run `ruff check .` and fix all linting errors across codebase
- [X] T047 Run `mypy src/` and fix all type checking errors
- [X] T048 Run `black .` to format all Python files consistently
- [X] T049 Run `uv run pytest --cov=src/tasks_cli --cov-report=term-missing` and verify ≥80% coverage (or implement additional tests if below threshold)
- [X] T050 Manual testing: Follow quickstart.md scenarios end-to-end on Windows, macOS, or Linux
- [X] T051 Verify all constitution principles: code quality (linting passing), testing (coverage ≥80%), UX (error messages clear), performance (<100ms add, <200ms list), documentation (README complete)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T010) completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (T011-T019) completion
- **User Story 2 (Phase 4)**: Depends on Foundational (T011-T019) completion - CAN run in parallel with US1 if desired
- **Polish (Phase 5)**: Depends on both User Stories 1 and 2 being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on User Story 1 (independently testable with pre-populated storage)

### Within Each Phase

**Phase 1 (Setup)**:
- T001-T003 sequential (project initialization)
- T004 after T003 (add dev dependencies after project exists)
- T005-T010 can all run in parallel after T001-T004 complete

**Phase 2 (Foundational)**:
- T011-T013 (Task model) can run in parallel - no dependencies
- T014-T017 (TaskStorage) sequential within themselves but parallel to Task model
- T018-T019 (CLI framework) can run in parallel with model/storage work

**Phase 3 (User Story 1)**:
- Tests (T020-T023) can all run in parallel - write all tests first
- T024 (add_task implementation) depends on T011-T017 (Task model and storage foundation)
- T025-T030 sequential, building on T024

**Phase 4 (User Story 2)**:
- Tests (T031-T033) can all run in parallel - write all tests first
- T034 (get_all_tasks) depends on T011-T017 (Task model and storage foundation)
- T035-T041 sequential, building on T034

**Phase 5 (Polish)**:
- T042-T045 (documentation) can run in parallel
- T046-T048 (linting/formatting) can run in parallel after code complete
- T049-T051 sequential (test, then manual validation, then constitution check)

### Parallel Opportunities

**Maximum Parallelization Strategy:**

1. **Phase 1**: Run T005-T010 simultaneously after T001-T004
2. **Phase 2**: Run T011-T013 (models) || T014-T017 (storage) || T018-T019 (CLI)
3. **Phase 3 + Phase 4**: After Phase 2, run BOTH user stories in parallel:
   - Team Member A: Complete User Story 1 (T020-T030)
   - Team Member B: Complete User Story 2 (T031-T041)
4. **Phase 5**: Run T042-T045 in parallel, then T046-T048, then T049-T051

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational tasks together after Setup completes:
Terminal 1: "Create Task model dataclass in src/tasks_cli/models/task.py"
Terminal 2: "Create TaskStorage class skeleton in src/tasks_cli/storage/task_storage.py"
Terminal 3: "Create CLI argparse setup in src/tasks_cli/cli.py"
```

---

## Parallel Example: User Story Work

```bash
# After Foundational phase, launch both user stories:
Developer A: "Implement User Story 1 (Add Tasks) - T020 through T030"
Developer B: "Implement User Story 2 (List Tasks) - T031 through T041"
# Both stories are independently testable and don't block each other
```

---

## Implementation Strategy

### MVP First (Recommended - User Story 1 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T019) - CRITICAL checkpoint
3. Complete Phase 3: User Story 1 (T020-T030) - Add functionality
4. **STOP and VALIDATE**: Test adding tasks end-to-end
5. **MVP READY**: Users can now capture tasks persistently
6. Optional: Continue to User Story 2 for list functionality

### Full Feature Delivery (Both User Stories)

1. Complete Phase 1: Setup → Foundation initialized
2. Complete Phase 2: Foundational → Core infrastructure ready
3. Complete Phase 3: User Story 1 → Can add tasks ✓
4. Complete Phase 4: User Story 2 → Can view tasks ✓
5. Complete Phase 5: Polish → Production-ready
6. **FULL FEATURE READY**: Complete task management workflow

### Parallel Team Strategy

With two developers:

1. Both complete Phase 1 + Phase 2 together (pair on foundation)
2. Once Foundational is done:
   - **Developer A**: User Story 1 (T020-T030) - Add functionality
   - **Developer B**: User Story 2 (T031-T041) - List functionality
3. Merge both stories (no conflicts - different commands)
4. Together: Complete Phase 5 (Polish)

---

## Task Count Summary

- **Phase 1 (Setup)**: 10 tasks
- **Phase 2 (Foundational)**: 9 tasks
- **Phase 3 (User Story 1)**: 11 tasks (7 optional test tasks + 7 implementation tasks = but tests are grouped, so 11 total)
- **Phase 4 (User Story 2)**: 11 tasks (3 optional test tasks + 8 implementation tasks = 11 total)
- **Phase 5 (Polish)**: 10 tasks

**Total**: 51 tasks
- **Without optional tests**: 37 tasks (core implementation only)
- **With optional tests**: 51 tasks (TDD approach)

---

## Validation Checklist

Before marking this feature complete, verify:

- ✅ All tasks checked off in this document
- ✅ `tasks add "description"` works and persists to ~/.tasks.json
- ✅ `tasks list` displays all tasks in alphabetical order (case-insensitive)
- ✅ Empty storage shows "No tasks found"
- ✅ Error messages are clear and actionable
- ✅ File corruption handled gracefully with backup
- ✅ Tests pass (if implemented): `uv run pytest`
- ✅ Linting passes: `ruff check .`
- ✅ Type checking passes: `mypy src/`
- ✅ Code coverage ≥80% (if tests implemented): `pytest --cov`
- ✅ Performance: Add <100ms, List <200ms (for typical usage)
- ✅ Cross-platform: Works on Windows/macOS/Linux
- ✅ README.md complete with installation and usage
- ✅ All constitution principles satisfied (code quality, testing, UX, performance, documentation)

---

## Notes

- **[P] tasks**: Different files, no dependencies - safe to parallelize
- **[Story] label**: Maps task to specific user story (US1 or US2) for traceability
- **Test-first approach**: If implementing tests, write them BEFORE implementation and ensure they fail
- **Incremental commits**: Commit after each task or logical group of tasks
- **Independent stories**: User Story 2 doesn't depend on User Story 1 implementation (can use pre-populated test data)
- **Constitution compliance**: All tasks align with code quality, testing, UX, performance, and documentation principles
- **MVP milestone**: Phase 1 + Phase 2 + Phase 3 = Minimal viable product (can add tasks)
- **Full feature**: All 5 phases = Complete task management with add and list functionality
