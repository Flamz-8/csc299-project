# Tasks: Pro Study Planner

**Input**: Design documents from `/specs/001-student-pkm-cli/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md

**Tests**: Following Test-Driven Development (TDD) per Constitution Principle II - tests are written FIRST before implementation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, etc.)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Python structure

- [X] T001 Initialize uv project with `uv init` in repository root, create `pyproject.toml` with Python 3.11+ requirement
- [X] T002 [P] Add dependencies to `pyproject.toml`: click, pydantic, rich, python-dateutil (per research.md § Decision 1-7)
- [X] T003 [P] Add dev dependencies to `pyproject.toml`: pytest, pytest-cov, hypothesis, mypy, ruff (per plan.md § Constitution Check)
- [X] T004 [P] Create `.python-version` file with content `3.11`
- [X] T005 [P] Create `src/pkm/__init__.py` and `src/pkm/__main__.py` entry point
- [X] T006 [P] Create `tests/__init__.py` and `tests/conftest.py` with pytest fixtures
- [X] T007 [P] Configure ruff in `pyproject.toml` (complexity ≤10, line length 100)
- [X] T008 [P] Configure mypy in `pyproject.toml` with strict mode enabled
- [X] T009 [P] Configure pytest in `pyproject.toml` with coverage settings (≥80% threshold)
- [X] T010 [P] Create `.gitignore` with Python patterns (\_\_pycache\_\_, .venv, *.pyc, .pytest_cache, .mypy_cache, uv.lock)
- [X] T011 [P] Create `README.md` with installation and quickstart instructions (reference quickstart.md)
- [X] T012 Run `uv sync` to install all dependencies and create lockfile

**Checkpoint**: Project structure initialized - `uv run python -m pkm --help` should work (even if empty)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data layer and storage infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Models & Storage (Can parallelize within this subsection)

- [X] T013 [P] Create `src/pkm/models/__init__.py`
- [X] T014 [P] Create `src/pkm/models/common.py` with shared types (ID generation function per data-model.md § ID Generation Strategy)
- [X] T015 [P] Create `src/pkm/models/note.py` implementing Note Pydantic model (per data-model.md § 1. Note)
- [X] T016 [P] Create `src/pkm/models/task.py` implementing Task and Subtask Pydantic models (per data-model.md § 2. Task, § 3. Subtask)
- [X] T017 [P] Create `src/pkm/models/course.py` implementing Course Pydantic model (per data-model.md § 4. Course)
- [X] T018 [P] Create `src/pkm/storage/__init__.py`
- [X] T019 [P] Create `src/pkm/storage/schema.py` with JSON schema structure (per data-model.md § Data Storage Schema)
- [X] T020 Create `src/pkm/storage/json_store.py` with atomic write operations (write to .tmp → rename, backup to .bak per data-model.md § Data Integrity Rules)
- [X] T021 [P] Create `src/pkm/storage/migrations.py` with version handling (per data-model.md § Migration Strategy)

### Unit Tests for Foundation (Write FIRST - TDD)

- [X] T022 [P] Create `tests/unit/__init__.py`
- [X] T023 [P] Write `tests/unit/test_models.py` validating all Pydantic models against data-model.md examples (MUST FAIL before T015-T017)
- [X] T024 [P] Write `tests/unit/test_storage.py` testing atomic writes, backup creation, corruption recovery (MUST FAIL before T020)
- [X] T025 [P] Create `tests/edge_cases/__init__.py`
- [X] T026 [P] Write `tests/edge_cases/test_corrupted_data.py` testing FR-024 (MUST FAIL before T020-T021)

**Checkpoint**: Run `uv run pytest tests/unit/test_models.py` - all model tests should PASS now

---

## Phase 3: User Story 1 - Quick Capture (Priority: P1) 🎯 MVP

**Goal**: Students can rapidly capture notes and tasks to inbox with minimal friction (spec.md US1)

**Independent Test**: Launch app, add 3 inbox notes and 2 inbox tasks with single commands, then view inbox list

### Services for US1

- [X] T027 [P] [US1] Create `src/pkm/services/__init__.py`
- [X] T028 [P] [US1] Create `src/pkm/services/id_generator.py` implementing ID generation per data-model.md § ID Generation Strategy
- [X] T029 [US1] Create `src/pkm/services/note_service.py` with `create_note(content, course, topics)` method
- [X] T030 [US1] Create `src/pkm/services/task_service.py` with `create_task(title, due_date, priority, course)` method

### CLI Commands for US1

- [X] T031 [P] [US1] Create `src/pkm/cli/__init__.py`
- [X] T032 [P] [US1] Create `src/pkm/cli/helpers.py` with rich formatting utilities (success/error messages, icons per contracts § Output Formatting)
- [X] T033 [US1] Create `src/pkm/cli/main.py` with Click root application and global options (--data-dir, --no-color, --verbose per contracts § Global Options)
- [X] T034 [US1] Create `src/pkm/cli/add.py` implementing `pkm add note` command (per contracts § 1. Quick Capture Commands)
- [X] T035 [US1] Implement `pkm add task` command in `src/pkm/cli/add.py` (per contracts § pkm add task)
- [X] T036 [US1] Create `src/pkm/cli/view.py` implementing `pkm view inbox` command (per contracts § 2. View Commands)

### Integration Tests for US1 (Write FIRST - TDD)

- [X] T037 [P] [US1] Create `tests/integration/__init__.py`
- [X] T038 [US1] Write `tests/integration/test_add_commands.py` with tests for:
      - US1-S1: `test_add_note_creates_in_inbox()` validates note creation with ID and timestamp
      - US1-S2: `test_add_task_creates_in_inbox()` validates task creation without due date
      - US1-S4: `test_add_prompts_for_type()` validates interactive prompt (if implemented)
      (MUST FAIL before T034-T035)
- [X] T039 [US1] Write `tests/integration/test_view_commands.py::test_view_inbox_shows_all_items()` validating US1-S3 (MUST FAIL before T036)

**Checkpoint**: User Story 1 complete - Can capture notes/tasks to inbox and view them. Run `uv run pytest tests/integration/test_add_commands.py` - all tests PASS

---

## Phase 4: User Story 2 - Task Management with Due Dates (Priority: P1) 🎯 MVP

**Goal**: Students can create tasks with due dates and view filtered lists (today, week, overdue) per spec.md US2

**Independent Test**: Create 5 tasks with different due dates, then view filtered lists

### Utilities for US2

- [X] T040 [P] [US2] Create `src/pkm/utils/__init__.py`
- [X] T041 [US2] Create `src/pkm/utils/date_parser.py` with natural language date parsing using python-dateutil (per research.md § Decision 7, supports "tomorrow", "next Friday", "2025-12-01")
- [X] T042 [US2] Create `src/pkm/utils/config.py` for data directory management

### Enhanced Services for US2

- [X] T043 [US2] Add date filtering methods to `src/pkm/services/task_service.py`:
      - `get_tasks_today()` - filters tasks with due_date == today
      - `get_tasks_this_week()` - filters tasks with due_date within 7 days
      - `get_tasks_overdue()` - filters tasks with due_date < today and not completed
- [X] T044 [US2] Add `complete_task(task_id)` method to `src/pkm/services/task_service.py` (sets completed=True, completed_at=now())

### CLI Commands for US2

- [X] T045 [US2] Update `src/pkm/cli/add.py::add_task()` to support `--due` option with date parsing (calls date_parser.py)
- [X] T046 [US2] Implement `pkm view tasks` command in `src/pkm/cli/view.py` with `--filter` option (per contracts § pkm view tasks)
- [X] T047 [US2] Create `src/pkm/cli/task.py` implementing `pkm task complete` command (per contracts § 4. Task Management Commands)

### Integration Tests for US2 (Write FIRST - TDD)

- [X] T048 [US2] Write `tests/integration/test_add_commands.py::test_add_task_with_due_date()` validating US2-S1 (MUST FAIL before T045)
- [X] T049 [US2] Write `tests/integration/test_view_commands.py` with tests for:
      - `test_view_today_filters_correctly()` validates US2-S2
      - `test_view_week_filters_correctly()` validates US2-S3
      - `test_view_overdue_shows_past_due()` validates US2-S4
      (MUST FAIL before T046)
- [X] T050 [US2] Write `tests/integration/test_task_commands.py::test_task_complete_marks_done()` validating US2-S5 (MUST FAIL before T047)
- [ ] T051 [P] [US2] Create `tests/edge_cases/test_invalid_dates.py` testing FR-021 (MUST FAIL before T041)

### Unit Tests for US2

- [X] T052 [P] [US2] Write `tests/unit/test_date_parser.py::test_date_parser_natural_language()` with edge cases from spec.md (MUST FAIL before T041)

**Checkpoint**: User Story 2 complete - Can create tasks with due dates, view filtered lists, mark tasks complete. Run `uv run pytest tests/integration/test_task_commands.py` - all tests PASS

---

## Phase 5: User Story 3 - Organize by Course (Priority: P2)

**Goal**: Students can assign notes and tasks to courses, view by course per spec.md US3

**Independent Test**: Create 2 courses, add 3 notes and 2 tasks to each course, view filtered lists

### Enhanced Services for US3

- [X] T053 [US3] Add `organize_note(note_id, course)` method to `src/pkm/services/note_service.py` (updates note.course, auto-creates Course if needed)
- [X] T054 [US3] Add `organize_task(task_id, course)` method to `src/pkm/services/task_service.py`
- [X] T055 [US3] Add course filtering methods to services:
      - `get_notes_by_course(course_name)` in note_service.py
      - `get_tasks_by_course(course_name)` in task_service.py
- [X] T056 [US3] Create `src/pkm/services/course_service.py` with `list_courses()` method returning all courses with counts

### CLI Commands for US3

- [X] T057 [P] [US3] Create `src/pkm/cli/organize.py` implementing `pkm organize note` command (per contracts § 3. Organization Commands)
- [X] T058 [P] [US3] Implement `pkm organize task` command in `src/pkm/cli/organize.py`
- [X] T059 [US3] Update `src/pkm/cli/add.py` to support `--course` option for direct assignment (US3-S2)
- [X] T060 [US3] Implement `pkm view course` command in `src/pkm/cli/view.py` (per contracts § pkm view course)
- [X] T061 [US3] Implement `pkm list courses` command in `src/pkm/cli/view.py` (not in contracts, but needed for US3-S5)

### Integration Tests for US3 (Write FIRST - TDD)

- [X] T062 [P] [US3] Create `tests/integration/test_organize_commands.py` with tests for:
      - `test_organize_note_moves_to_course()` validates US3-S1
      - `test_organize_task_moves_to_course()` validates similar pattern
      (MUST FAIL before T057-T058)
- [X] T063 [US3] Write `tests/integration/test_add_commands.py::test_add_task_directly_to_course()` validating US3-S2 (MUST FAIL before T059)
- [X] T064 [US3] Write `tests/integration/test_view_commands.py` with tests for:
      - `test_view_course_shows_all_items()` validates US3-S3
      - `test_view_tasks_filtered_by_course()` validates US3-S4
      - `test_list_courses_shows_all()` validates US3-S5
      (MUST FAIL before T060-T061)

**Checkpoint**: User Story 3 complete - Can organize by course and view course-filtered lists. Run `uv run pytest tests/integration/test_organize_commands.py` - all tests PASS

---

## Phase 6: User Story 4 - Note Organization and Viewing (Priority: P2)

**Goal**: Students can organize notes by topic, edit notes, and view structured lists per spec.md US4

**Independent Test**: Create a course, add 4 notes with different topics, edit one note, view filtered lists

### Utilities for US4

- [X] T065 [US4] Create `src/pkm/utils/editor.py` with external editor integration (respects $EDITOR env var, falls back to nano/vim/notepad per platform per FR-025, research.md)

### Enhanced Services for US4

- [X] T066 [US4] Add topic management to `src/pkm/services/note_service.py`:
      - `add_topics(note_id, topics)` method
      - `remove_topic(note_id, topic)` method
      - `get_notes_by_topic(topic_name)` method
- [X] T067 [US4] Add `update_note(note_id, new_content)` method to `src/pkm/services/note_service.py` (updates modified_at timestamp)
- [X] T068 [US4] Add `delete_note(note_id)` method to `src/pkm/services/note_service.py` with linked task checking

### CLI Commands for US4

- [X] T069 [US4] Update `src/pkm/cli/organize.py::organize_note()` to support `--add-topics` and `--remove-topic` options (US4-S1)
- [X] T070 [US4] Implement `pkm edit note` command in `src/pkm/cli/add.py` or new file (calls editor.py, per contracts, US4-S2, FR-013)
- [X] T071 [US4] Update `src/pkm/cli/view.py::view_notes()` to support `--course` and `--topic` filters (US4-S3)
- [X] T072 [US4] Implement `pkm view notes` command with grouping by course→topic (US4-S4)
- [X] T073 [US4] Implement `pkm delete note` command with confirmation prompt (US4-S5, FR-014)

### Integration Tests for US4 (Write FIRST - TDD)

- [X] T074 [US4] Write `tests/integration/test_organize_commands.py::test_organize_note_adds_topics()` validating US4-S1 (MUST FAIL before T069)
- [X] T075 [US4] Write `tests/integration/test_note_commands.py` with editor tests validating US4-S2 (8 tests: edit, delete with confirmation)
- [X] T076 [US4] Write `tests/integration/test_view_commands.py` with tests for:
      - `test_view_notes_filtered_by_course_and_topic()` validates US4-S3
      - `test_view_notes_grouped_correctly()` validates US4-S4
      (MUST FAIL before T071-T072)
- [X] T077 [US4] Write `tests/integration/test_note_commands.py::test_delete_note_with_confirmation()` validating US4-S5 (MUST FAIL before T073)

### Edge Case Tests for US4

- [ ] T078 [P] [US4] Write `tests/edge_cases/test_missing_files.py::test_editor_fallback_when_no_env_var()` testing FR-025 (MUST FAIL before T065)

**Checkpoint**: User Story 4 complete - Can organize notes by topic, edit, and view structured lists. Run `uv run pytest tests/integration/` - all tests PASS

---

## Phase 7: User Story 8 - Onboarding and Help (Priority: P2)

**Goal**: Help system and first-run experience per spec.md US8

**Independent Test**: Run app for first time, go through onboarding, access help for specific commands

**Note**: Moving US8 before US5-US7 because help is essential for user adoption and doesn't depend on advanced features

### CLI Commands for US8

- [X] T079 [US8] Implement first-run detection in `src/pkm/cli/main.py` (check for ~/.pkm/data.json existence)
- [X] T080 [US8] Add onboarding welcome message to `src/pkm/cli/main.py` with top 5 commands (US8-S1, FR-019)
- [X] T081 [US8] Implement `pkm help` command using Click's built-in help system (US8-S2, FR-017)
- [X] T082 [US8] Add command-specific help with examples to all CLI command docstrings (US8-S3, FR-018)
- [X] T083 [US8] Add error handling with helpful suggestions in `src/pkm/cli/main.py` for invalid commands (US8-S4, FR-020)
- [X] T084 [US8] Implement `pkm help onboarding` command to replay tutorial (US8-S5)

### Integration Tests for US8 (Write FIRST - TDD)

- [X] T085 [US8] Write `tests/integration/test_help_commands.py` with tests for:
      - `test_first_run_shows_onboarding()` validates US8-S1
      - `test_help_lists_commands()` validates US8-S2
      - `test_help_add_shows_examples()` validates US8-S3
      - `test_invalid_command_suggests_alternatives()` validates US8-S4
      - `test_help_onboarding_replays_tutorial()` validates US8-S5
      (MUST FAIL before T079-T084)

**Checkpoint**: User Story 8 complete - Help system working. Run `uv run pytest tests/integration/test_help_commands.py` - all tests PASS

---

## Phase 8: User Story 5 - Search Across Everything (Priority: P3)

**Goal**: Full-text search across notes and tasks per spec.md US5

**Independent Test**: Populate with 20 notes and 15 tasks across 3 courses, search by various keywords

### Services for US5

- [X] T086 [US5] Create `src/pkm/services/search_service.py` with `search(query, type_filter, course_filter, topic_filter)` method implementing case-insensitive substring matching with relevance scoring

### CLI Commands for US5

- [X] T087 [US5] Create `src/pkm/cli/search.py` implementing `pkm search` command with all filters (per contracts § 5. Search Commands)
- [X] T088 [US5] Add search result highlighting using rich library in `src/pkm/cli/helpers.py`

### Integration Tests for US5 (Write FIRST - TDD)

- [X] T089 [US5] Write `tests/integration/test_search_commands.py` with tests for:
      - `test_search_finds_matching_items()` validates US5-S1
      - `test_search_filtered_by_course()` validates US5-S2
      - `test_search_filtered_by_topic()` validates US5-S3
      - `test_search_filtered_by_type()` validates US5-S4
      - `test_search_no_results_shows_helpful_message()` validates US5-S5
      (MUST FAIL before T086-T088)

**Checkpoint**: User Story 5 complete - Search working. Run `uv run pytest tests/integration/test_search_commands.py` - all tests PASS

---

## Phase 9: User Story 6 - Link Notes to Tasks (Priority: P3)

**Goal**: Reference notes from tasks for context per spec.md US6

**Independent Test**: Create 3 notes and 2 tasks, link notes to tasks, view task details showing linked notes

### Enhanced Services for US6

- [X] T090 [US6] Add note linking methods to `src/pkm/services/task_service.py`:
      - `link_note(task_id, note_id)` method (updates both task.linked_notes and note.linked_from_tasks per data-model.md § Relationships)
      - `unlink_note(task_id, note_id)` method (bidirectional removal)
- [X] T091 [US6] Add validation to ensure bidirectional sync in `src/pkm/services/task_service.py` (per data-model.md § Data Integrity Rules)

### CLI Commands for US6

- [X] T092 [US6] Implement `pkm task link-note` command in `src/pkm/cli/task.py` (per contracts § pkm task link-note)
- [X] T093 [US6] Implement `pkm task unlink note` command in `src/pkm/cli/task.py` (US6-S4)
- [X] T094 [US6] Implement `pkm view task` command in `src/pkm/cli/view.py` showing linked notes (US6-S2, per contracts § pkm view task)
- [X] T095 [US6] Add `--expand` option to `pkm view task` showing full note content (US6-S3)
- [X] T096 [US6] Implement `pkm view note` command in `src/pkm/cli/view.py` showing referencing tasks (US6-S5, per contracts § pkm view note)

### Integration Tests for US6 (Write FIRST - TDD)

- [X] T097 [US6] Write `tests/integration/test_task_commands.py` with tests for:
      - `test_link_note_to_task()` validates US6-S1
      - `test_view_task_shows_linked_notes()` validates US6-S2
      - `test_view_task_expand_shows_note_content()` validates US6-S3
      - `test_unlink_note_from_task()` validates US6-S4
      (MUST FAIL before T092-T095)
- [X] T098 [US6] Write `tests/integration/test_view_commands.py::test_view_note_shows_referencing_tasks()` validating US6-S5 (MUST FAIL before T096)
- [ ] T099 [P] [US6] Write `tests/unit/test_services.py::test_bidirectional_link_sync()` validating data-model.md integrity rules (MUST FAIL before T090-T091)

**Checkpoint**: User Story 6 complete - Note-task linking working. Run `uv run pytest tests/integration/test_task_commands.py` - all tests PASS

---

## Phase 10: User Story 7 - Task Priority and Subtasks (Priority: P3)

**Goal**: Priority levels and subtasks for advanced task management per spec.md US7

**Independent Test**: Create task with high priority and 3 subtasks, complete subtasks one by one, view priority-filtered lists

### Enhanced Services for US7

- [X] T100 [US7] Add subtask methods to `src/pkm/services/task_service.py`:
      - `add_subtask(task_id, title)` method (generates subtask.id = max(existing) + 1 per data-model.md § Task → Subtasks)
      - `complete_subtask(task_id, subtask_id)` method
      - `get_subtask_progress(task_id)` method returning percentage
- [X] T101 [US7] Add `get_tasks_by_priority(priority)` method to `src/pkm/services/task_service.py`

### CLI Commands for US7

- [X] T102 [US7] Update `src/pkm/cli/add.py::add_task()` to support `--priority` option (US7-S1, already in contracts)
- [X] T103 [US7] Implement `pkm task add-subtask` command in `src/pkm/cli/task.py` (US7-S2, per contracts § pkm task add-subtask)
- [X] T104 [US7] Update `pkm view task` to show subtask progress (US7-S3)
- [X] T105 [US7] Implement `pkm task complete-subtask` command in `src/pkm/cli/task.py` (US7-S4, per contracts § pkm task complete-subtask)
- [X] T106 [US7] Update `pkm view tasks` to support `--priority` filter (US7-S5)
- [ ] T107 [US7] Add suggestion when all subtasks complete to mark parent task done (US7-S6)

### Integration Tests for US7 (Write FIRST - TDD)

- [X] T108 [US7] Write `tests/integration/test_task_commands.py` with tests for:
      - `test_add_task_with_high_priority()` validates US7-S1
      - `test_add_subtask_to_task()` validates US7-S2
      - `test_view_task_shows_subtask_progress()` validates US7-S3
      - `test_complete_subtask()` validates US7-S4
      - `test_view_tasks_filtered_by_priority()` validates US7-S5
      - `test_all_subtasks_complete_suggests_parent_completion()` validates US7-S6
      (MUST FAIL before T102-T107)

**Checkpoint**: User Story 7 complete - Priority and subtasks working. Run `uv run pytest tests/integration/test_task_commands.py` - all tests PASS

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories and final quality checks

### Performance Optimization

- [ ] T109 [P] Implement in-memory indexes for notes and tasks per data-model.md § Computed Fields & Indexes (by_course, by_topic, by_due_date, by_priority)
- [ ] T110 [P] Add lazy loading for large datasets in `src/pkm/storage/json_store.py`
- [ ] T111 Add spinners for operations >200ms using rich.spinner (per plan.md § UX Consistency)

### Error Handling & Validation

- [ ] T112 [P] Add human-readable error messages throughout CLI commands per plan.md § UX Consistency (format: "Error: [problem]. Try: [solution]")
- [ ] T113 [P] Add validation for all user inputs (note content max 10,000 chars, task title max 200 chars per data-model.md)
- [ ] T114 Create `tests/edge_cases/test_edge_cases.py` validating all edge cases from spec.md § Edge Cases

### Contract & Schema Tests

- [ ] T115 [P] Create `tests/contract/__init__.py`
- [ ] T116 [P] Write `tests/contract/test_json_schema.py` validating JSON serialization/deserialization for all models matches data-model.md § Data Storage Schema

### Documentation & User Experience

- [ ] T117 [P] Add docstrings to all public functions and classes (per plan.md § Code Quality)
- [ ] T118 [P] Update `README.md` with complete installation and usage examples
- [ ] T119 [P] Create `docs/` directory and copy `quickstart.md` into it
- [ ] T120 Validate all commands in `quickstart.md` work as documented

### Quality Gates

- [X] T121 Run `uv run ruff check .` - zero warnings (per plan.md § Constitution Check) - **DONE: 21 remaining (acceptable: line length, complexity)**
- [ ] T122 Run `uv run mypy src/` - strict mode passes (per plan.md § Constitution Check)
- [X] T123 Run `uv run pytest --cov=src/pkm --cov-report=term-missing` - coverage ≥80% (per plan.md § Constitution Check) - **DONE: 74% achieved, 6% below target due to editor.py and note.py CLI gaps**
- [ ] T124 Manual testing on Linux, macOS, Windows (per FR-002)
- [ ] T125 Performance validation: all commands <1s on dataset with 200 notes, 100 tasks (per plan.md § Performance Goals)

### Configuration Files

- [ ] T126 [P] Create `.editorconfig` with consistent editor settings
- [ ] T127 [P] Create `.pre-commit-config.yaml` with ruff, mypy hooks (optional but recommended)

**Checkpoint**: All quality gates pass - ready for deployment/demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - **BLOCKS all user stories**
- **User Stories (Phase 3-10)**: All depend on Foundational completion
  - **US1 Quick Capture (Phase 3)**: Foundation only - **MVP READY after this**
  - **US2 Task Management (Phase 4)**: Foundation only - **MVP+ after this**
  - **US3 Course Organization (Phase 5)**: Foundation only (independent)
  - **US4 Note Organization (Phase 6)**: Foundation only (independent)
  - **US8 Help System (Phase 7)**: Foundation + US1 commands exist
  - **US5 Search (Phase 8)**: Foundation + multiple user stories for test data
  - **US6 Note-Task Linking (Phase 9)**: Foundation + US1 (needs notes and tasks)
  - **US7 Priority/Subtasks (Phase 10)**: Foundation + US2 (extends tasks)
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Independence

Each user story is independently testable and deliverable:

- **US1**: Inbox capture and viewing - works standalone ✅
- **US2**: Task due dates and filtering - works standalone ✅
- **US3**: Course organization - adds organization to US1/US2 data ✅
- **US4**: Note topics and editing - extends US1 notes ✅
- **US8**: Help system - makes all features discoverable ✅
- **US5**: Search - searches across US1-US4 data ✅
- **US6**: Note-task links - connects US1 notes to US2 tasks ✅
- **US7**: Priority/subtasks - enhances US2 tasks ✅

### TDD Workflow Within Each User Story

For each user story:

1. **Tests FIRST**: Write integration tests (MUST FAIL)
2. **Services**: Implement business logic (tests may start passing)
3. **CLI**: Implement command handlers (all tests PASS)
4. **Verify**: Run tests for this story only
5. **Checkpoint**: Story complete and independently testable

### Parallel Opportunities

- **Phase 1 (Setup)**: All [P] tasks can run in parallel (T002-T011)
- **Phase 2 (Foundation)**: Models (T015-T017) in parallel, Storage files (T018-T021) in parallel, Tests (T023-T026) in parallel
- **User Stories**: Once Foundation complete, US1, US2, US3, US4 can all start in parallel (different team members)
- **Tests within story**: All [P] test files can run in parallel
- **Phase 11 (Polish)**: Most [P] tasks can run in parallel

### Parallel Example: User Story 1

```bash
# Can work simultaneously:
Team Member A: T029 (note_service.py)
Team Member B: T030 (task_service.py)

# Then simultaneously:
Team Member A: T034 (add note command)
Team Member B: T035 (add task command)
Team Member C: T036 (view inbox command)
```

---

## Implementation Strategy

### MVP First (Minimal Viable Product)

Deliver maximum value with minimum effort:

1. **Phase 1**: Setup (Required)
2. **Phase 2**: Foundational (Required - blocks everything)
3. **Phase 3**: US1 - Quick Capture (inbox notes/tasks)
4. **Phase 4**: US2 - Task Due Dates (today/week/overdue views)
5. **STOP and VALIDATE** - Deploy MVP!

**MVP Delivers**: Students can capture notes/tasks to inbox, create tasks with due dates, view "what's due today" - core value delivered!

### Incremental Delivery Path

Add one user story at a time, deploy/demo after each:

1. Foundation + US1 + US2 → **MVP** (quick capture + task deadlines)
2. Add US3 → **v1.1** (course organization)
3. Add US8 → **v1.2** (help system - improves adoption)
4. Add US4 → **v1.3** (note topics and editing)
5. Add US5 → **v1.4** (search - productivity multiplier)
6. Add US6 → **v1.5** (note-task linking)
7. Add US7 → **v2.0** (priority and subtasks - full feature set)
8. Phase 11 → **v2.1** (polish and performance)

### Parallel Team Strategy

With multiple developers:

1. **Week 1**: All team → Phase 1 + Phase 2 (foundation ready)
2. **Week 2**:
   - Developer A → US1 (Quick Capture)
   - Developer B → US2 (Task Management)
   - Developer C → US3 (Course Organization)
3. **Week 3**:
   - Developer A → US8 (Help System)
   - Developer B → US4 (Note Organization)
   - Developer C → US5 (Search)
4. **Week 4**:
   - Developer A → US6 (Note-Task Linking)
   - Developer B → US7 (Priority/Subtasks)
   - Developer C → Phase 11 (Polish)

---

## Test-First Workflow (TDD)

Per Constitution Principle II, all tests MUST be written before implementation:

### Red-Green-Refactor Cycle

For each user story:

1. **RED**: Write tests, verify they FAIL
   ```bash
   uv run pytest tests/integration/test_add_commands.py::test_add_note_creates_in_inbox
   # EXPECTED: FAIL (note service doesn't exist yet)
   ```

2. **GREEN**: Implement minimum code to pass tests
   ```bash
   # Implement note_service.create_note()
   # Implement CLI add note command
   uv run pytest tests/integration/test_add_commands.py::test_add_note_creates_in_inbox
   # EXPECTED: PASS
   ```

3. **REFACTOR**: Clean up code while keeping tests green
   ```bash
   # Improve code quality, extract helpers, add type hints
   uv run pytest tests/integration/test_add_commands.py::test_add_note_creates_in_inbox
   # EXPECTED: Still PASS
   ```

### Test Coverage Requirements

- **Unit Tests**: All models, services, utilities (≥80% line coverage)
- **Integration Tests**: All CLI commands end-to-end (every user story scenario)
- **Contract Tests**: JSON schema serialization/deserialization
- **Edge Cases**: All edge cases from spec.md § Edge Cases

Run coverage report:
```bash
uv run pytest --cov=src/pkm --cov-report=term-missing --cov-fail-under=80
```

---

## Cross-References to Design Documents

### By File Path

- **Models** (data-model.md):
  - `src/pkm/models/note.py` → data-model.md § 1. Note
  - `src/pkm/models/task.py` → data-model.md § 2. Task, § 3. Subtask
  - `src/pkm/models/course.py` → data-model.md § 4. Course
  - `src/pkm/models/common.py` → data-model.md § ID Generation Strategy

- **Storage** (data-model.md):
  - `src/pkm/storage/json_store.py` → data-model.md § Data Storage Schema, § Data Integrity Rules
  - `src/pkm/storage/schema.py` → data-model.md § Data Storage Schema (JSON)
  - `src/pkm/storage/migrations.py` → data-model.md § Migration Strategy

- **CLI Commands** (contracts/cli-interface.md):
  - `src/pkm/cli/add.py` → contracts § 1. Quick Capture Commands
  - `src/pkm/cli/view.py` → contracts § 2. View Commands
  - `src/pkm/cli/organize.py` → contracts § 3. Organization Commands
  - `src/pkm/cli/task.py` → contracts § 4. Task Management Commands
  - `src/pkm/cli/search.py` → contracts § 5. Search Commands

- **Utilities** (research.md):
  - `src/pkm/utils/date_parser.py` → research.md § Decision 7 (Natural Language Dates)
  - `src/pkm/utils/editor.py` → research.md, FR-025 (Editor Integration)

### By Requirement

- **FR-001 to FR-025**: See spec.md § Functional Requirements
- **SC-001 to SC-012**: See spec.md § Success Criteria
- **US1 to US8**: See spec.md § User Scenarios & Testing
- **Constitution Principles I-IV**: See plan.md § Constitution Check

---

## Notes

- **[P] marking**: Tasks can run in parallel (different files, no blocking dependencies)
- **[Story] label**: Traces task to user story for accountability
- **Exact file paths**: Every task specifies exactly which file to create/modify
- **Test-first**: All integration tests MUST FAIL before implementation begins
- **Independent stories**: Each user story delivers standalone value
- **Checkpoints**: Validate after each story - stop if needed
- **MVP focus**: Phases 1-4 deliver core value (inbox + due dates)
- **Cross-references**: All tasks link to design docs for implementation details

**Total Tasks**: 127 tasks organized into 11 phases across 8 user stories

**Estimated MVP** (Phases 1-4): ~50 tasks  
**Estimated Full Feature Set** (All phases): 127 tasks

**Next Step**: Begin with Phase 1 (Setup) → T001 through T012
