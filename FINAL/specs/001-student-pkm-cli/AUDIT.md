# Implementation Plan Audit: Pro Study Planner

**Date**: 2025-11-23  
**Auditor**: GitHub Copilot  
**Purpose**: Assess completeness of implementation plan and identify gaps for task generation

---

## Executive Summary

### ✅ Strengths
- **Comprehensive architecture**: Clear separation of concerns (models, services, CLI, storage)
- **Well-documented contracts**: CLI interface is thoroughly specified with examples
- **Strong data model**: All 6 entities clearly defined with relationships
- **Constitution compliance**: All 4 principles validated with specific tooling
- **User-centric spec**: 8 user stories with acceptance criteria and priorities

### ⚠️ Critical Gaps
1. **No implementation task breakdown** - tasks.md does not exist yet
2. **Missing cross-references** - Plan doesn't link to specific sections of detail docs
3. **No implementation sequence** - Unclear which files to build first
4. **Incomplete dependency mapping** - Service/model dependencies not explicitly charted
5. **Test strategy lacks specifics** - No concrete test file → requirement mapping

---

## Document Completeness Analysis

### 1. spec.md ✅ COMPLETE
**Status**: Comprehensive, well-structured

**Contents**:
- ✅ 8 user stories with priorities (P1, P2, P3)
- ✅ 40+ acceptance scenarios across all stories
- ✅ 25 functional requirements (FR-001 to FR-025)
- ✅ 6 key entities defined
- ✅ 12 success criteria with measurable outcomes
- ✅ Edge cases documented
- ✅ Out of scope clearly defined
- ✅ Dependencies and constraints identified

**Gaps**:
- ⚠️ No mapping of requirements to implementation files
- ⚠️ No explicit testing checklist per requirement

---

### 2. plan.md ⚠️ NEEDS ENHANCEMENT
**Status**: Architecture complete, execution guidance missing

**Contents**:
- ✅ Technical stack defined (Python 3.11+, uv, Click, Pydantic, rich)
- ✅ Constitution Check passed
- ✅ Project structure documented
- ✅ Performance budgets set
- ✅ Cross-platform constraints identified

**Gaps**:
- ❌ **No implementation roadmap**: Which files to build in which order?
- ❌ **No cross-references**: Doesn't point to data-model.md or contracts/ for details
- ❌ **No dependency tree**: Service → Model dependencies not visualized
- ❌ **No test-to-code mapping**: Which test files validate which features?
- ⚠️ **Missing setup instructions**: How to initialize the uv project?

**Recommended Additions**:

```markdown
## Implementation Roadmap (SUGGESTED)

### Phase 1: Foundation (No dependencies)
**Goal**: Basic project structure and data layer

**Files to create** (can be done in parallel):
1. `src/pkm/models/common.py` - Shared types (see data-model.md § ID Generation)
2. `src/pkm/models/note.py` - Note entity (see data-model.md § 1. Note)
3. `src/pkm/models/task.py` - Task entity (see data-model.md § 2. Task)
4. `src/pkm/models/course.py` - Course entity (see data-model.md § 4. Course)
5. `src/pkm/storage/schema.py` - JSON schema (see data-model.md § Data Storage Schema)
6. `src/pkm/storage/json_store.py` - File I/O (see research.md § Decision 6)

**Tests to write FIRST**:
- `tests/unit/test_models.py` - Validate Pydantic models against data-model.md examples
- `tests/unit/test_storage.py` - Atomic write tests, corruption recovery (FR-024)

**Reference docs**: data-model.md (entities), research.md § Decision 6 (JSON storage)

---

### Phase 2: Services (Depends on Phase 1 models)
**Goal**: Business logic layer

**Files to create**:
1. `src/pkm/services/id_generator.py` - Unique ID generation (see data-model.md § ID Generation Strategy)
2. `src/pkm/services/note_service.py` - Note operations (see data-model.md § Relationships)
3. `src/pkm/services/task_service.py` - Task operations (see data-model.md § Task → Subtasks)
4. `src/pkm/services/search_service.py` - Search logic (see spec.md US5)

**Tests to write FIRST**:
- `tests/unit/test_services.py` - Service method unit tests
- `tests/integration/test_note_task_linking.py` - Bidirectional link sync (data-model.md § Relationships)

**Reference docs**: data-model.md § Relationships, spec.md User Stories 1-5

---

### Phase 3: CLI Commands (Depends on Phase 2 services)
**Goal**: User-facing interface

**Files to create** (map to user stories):
1. `src/pkm/cli/add.py` - Quick capture (see contracts/ § 1. Quick Capture Commands)
   - Maps to: spec.md US1 (Quick Capture)
   - Implements: FR-003, FR-004, FR-005
   - Tests: `tests/integration/test_add_commands.py`

2. `src/pkm/cli/view.py` - Viewing commands (see contracts/ § 2. View Commands)
   - Maps to: spec.md US2 (Task Management), US4 (Note Viewing)
   - Implements: FR-010, FR-023
   - Tests: `tests/integration/test_view_commands.py`

3. `src/pkm/cli/organize.py` - Organization (see contracts/ § 3. Organization Commands)
   - Maps to: spec.md US3 (Course Organization), US4 (Topics)
   - Implements: FR-006, FR-007
   - Tests: `tests/integration/test_organize_commands.py`

4. `src/pkm/cli/task.py` - Task operations (see contracts/ § 4. Task Management Commands)
   - Maps to: spec.md US2 (Complete tasks), US6 (Linking), US7 (Subtasks)
   - Implements: FR-008, FR-009, FR-011
   - Tests: `tests/integration/test_task_commands.py`

5. `src/pkm/cli/search.py` - Search (see contracts/ § 5. Search Commands)
   - Maps to: spec.md US5 (Search)
   - Implements: FR-012
   - Tests: `tests/integration/test_search_commands.py`

**Reference docs**: contracts/cli-interface.md (all command contracts)

---

### Phase 4: Utilities (Can be done alongside Phase 3)
**Goal**: Supporting features

**Files to create**:
1. `src/pkm/utils/date_parser.py` - Natural language dates (see research.md § Decision 7)
2. `src/pkm/utils/editor.py` - External editor integration (FR-013, FR-025)
3. `src/pkm/utils/config.py` - Configuration management

**Tests to write FIRST**:
- `tests/unit/test_utils.py` - Date parsing edge cases (spec.md Edge Cases)
- `tests/edge_cases/test_invalid_dates.py` - Invalid date handling (FR-021)

**Reference docs**: research.md § Decision 7, spec.md § Edge Cases

---

### Dependency Tree

```
CLI Layer (Phase 3)
    ↓ depends on
Services Layer (Phase 2)
    ↓ depends on
Models + Storage (Phase 1)
```

**Parallel Work Opportunities**:
- Phase 1: All models can be built in parallel
- Phase 2: Services can be built in parallel after models exist
- Phase 3: Each CLI command file can be built in parallel after services exist
- Phase 4: Utilities can be built anytime (used by multiple layers)
```

---

### 3. data-model.md ✅ EXCELLENT
**Status**: Comprehensive reference document

**Contents**:
- ✅ Entity Relationship Diagram
- ✅ All 6 entities with complete schemas
- ✅ Pydantic examples for each entity
- ✅ Validation rules clearly defined
- ✅ ID generation strategy explained
- ✅ JSON storage schema with examples
- ✅ Relationship management patterns
- ✅ Data integrity rules
- ✅ Migration strategy

**Gaps**:
- ⚠️ No explicit "what to implement first" guidance
- ⚠️ Could add file path references (e.g., "Implement in `src/pkm/models/note.py`")

---

### 4. contracts/cli-interface.md ✅ EXCELLENT
**Status**: Comprehensive API specification

**Contents**:
- ✅ 15 commands fully specified
- ✅ Input/output contracts with examples
- ✅ Error handling patterns
- ✅ Exit codes defined
- ✅ Performance targets per command
- ✅ Global options documented

**Gaps**:
- ⚠️ No mapping to implementation files (which file implements which command?)
- ⚠️ No test specification (what assertions to make?)

---

### 5. research.md ✅ GOOD
**Status**: Technical decisions documented

**Contents**:
- ✅ 10 technical decisions with rationales
- ✅ Alternatives considered
- ✅ Constitution alignment verified
- ✅ Performance optimization strategies

**Gaps**:
- ⚠️ No "how to implement" guidance (just "what" and "why", not "how")
- ⚠️ Could add code snippets for key patterns

---

### 6. quickstart.md ✅ EXCELLENT
**Status**: User-facing documentation complete

**Contents**:
- ✅ Installation instructions
- ✅ 5 common workflows
- ✅ Sample data walkthrough
- ✅ Troubleshooting guide
- ✅ Top 5 commands reference

**Gaps**:
- None (this is end-user documentation, not implementation guidance)

---

### 7. tasks.md ❌ MISSING
**Status**: CRITICAL GAP - Not yet created

**What's Needed**:
A sequential task list that:
1. Maps user stories to implementation tasks
2. Specifies exact file paths for each task
3. Identifies dependencies between tasks
4. Links each task to relevant spec/data-model/contract sections
5. Provides test-first workflow (write test → implement → pass test)
6. Groups tasks by implementation phase
7. Marks parallelizable tasks

**Example Format** (from tasks-template.md):
```markdown
## Phase 1: Foundation

- [ ] T001 Create `pyproject.toml` with dependencies from research.md § Decision 2
- [ ] T002 [P] Implement Note model in `src/pkm/models/note.py` per data-model.md § 1. Note
- [ ] T003 [P] Implement Task model in `src/pkm/models/task.py` per data-model.md § 2. Task
- [ ] T004 Write unit tests in `tests/unit/test_models.py` validating data-model.md examples
      **Test-first**: These tests MUST fail before T002/T003, pass after

## Phase 2: Services

- [ ] T005 [US1] Implement NoteService.create() in `src/pkm/services/note_service.py`
      **Validates**: spec.md US1 Scenario 1 (create note in inbox)
      **Depends on**: T002 (Note model)
      **Tests**: tests/integration/test_add_commands.py::test_add_note_to_inbox
```

---

## Missing Cross-References

### In plan.md, add links like:

```markdown
## Technical Context

**Data Entities**: See [data-model.md](./data-model.md) for complete schemas
**CLI Commands**: See [contracts/cli-interface.md](./contracts/cli-interface.md) for all command contracts
**Technical Decisions**: See [research.md](./research.md) for rationale on Python/uv/Click choices

## Implementation Sequence

1. **Models Layer**: Implement entities per [data-model.md § Core Entities](./data-model.md#core-entities)
2. **Storage Layer**: Implement JSON persistence per [data-model.md § Data Storage Schema](./data-model.md#data-storage-schema)
3. **Services Layer**: Implement business logic per [data-model.md § Relationships](./data-model.md#relationships)
4. **CLI Layer**: Implement commands per [contracts/cli-interface.md](./contracts/cli-interface.md)
```

---

### In data-model.md, add implementation hints:

```markdown
### 1. Note

**Purpose**: Captures information, lecture notes, ideas, or references.

**Implementation File**: `src/pkm/models/note.py`

**Pydantic Model**:
```python
# src/pkm/models/note.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Note(BaseModel):
    id: str = Field(..., pattern=r"^n_\d{8}_\d{6}_[a-z0-9]{3}$")
    content: str = Field(..., min_length=1, max_length=10000)
    # ... (rest of fields from current doc)
```

**Referenced by**:
- spec.md FR-003 (create notes)
- spec.md US1 Scenario 1 (quick capture)
- contracts/cli-interface.md § `pkm add note`

**Tests**:
- tests/unit/test_models.py::test_note_validation
- tests/contract/test_json_schema.py::test_note_json_serialization
```

---

### In contracts/cli-interface.md, add implementation hints:

```markdown
#### `pkm add note [CONTENT]`

**Implementation File**: `src/pkm/cli/add.py` (function: `add_note`)

**Service Method**: `note_service.create_note(content, course, topics)`  
**Reference**: data-model.md § 1. Note

**Test Coverage**:
- Integration: `tests/integration/test_add_commands.py::test_add_note_to_inbox`
- Edge Case: `tests/edge_cases/test_empty_content.py::test_reject_empty_note`

**Validates**:
- spec.md FR-003 (create notes)
- spec.md US1 Scenario 1 (quick capture)
```

---

## Test Strategy Gaps

### Current State
- ✅ 4 test categories identified (unit, integration, contract, edge cases)
- ✅ Coverage target defined (80%+ line coverage)
- ✅ Test independence verified (pytest fixtures)

### Missing
- ❌ **No test file inventory**: Which specific test files to create?
- ❌ **No requirement → test mapping**: Which tests validate which FRs?
- ❌ **No acceptance → test mapping**: Which tests validate which scenarios?

### Recommended Test Mapping

```markdown
## Test Coverage Map

### User Story 1: Quick Capture

**Acceptance Scenarios → Tests**:
- US1-S1: `tests/integration/test_add_commands.py::test_add_note_creates_in_inbox`
- US1-S2: `tests/integration/test_add_commands.py::test_add_task_creates_in_inbox`
- US1-S3: `tests/integration/test_view_commands.py::test_view_inbox_shows_all_items`
- US1-S4: `tests/integration/test_add_commands.py::test_add_prompts_for_type`

**Functional Requirements → Tests**:
- FR-003: `tests/unit/test_services.py::test_note_service_create`
- FR-004: `tests/unit/test_services.py::test_task_service_create`
- FR-005: `tests/integration/test_view_commands.py::test_inbox_contains_unorganized`

### User Story 2: Task Management

**Acceptance Scenarios → Tests**:
- US2-S1: `tests/integration/test_add_commands.py::test_add_task_with_due_date`
- US2-S2: `tests/integration/test_view_commands.py::test_view_today_filters_correctly`
- US2-S3: `tests/integration/test_view_commands.py::test_view_week_filters_correctly`
- US2-S4: `tests/integration/test_view_commands.py::test_view_overdue_shows_past_due`
- US2-S5: `tests/integration/test_task_commands.py::test_task_complete_marks_done`

**Functional Requirements → Tests**:
- FR-010: `tests/unit/test_services.py::test_task_service_filter_by_date_range`
- FR-011: `tests/unit/test_services.py::test_task_service_mark_complete`

... (continue for all 8 user stories)
```

---

## Constitution Compliance Enhancement

### Current State
- ✅ All 4 principles checked
- ✅ Tooling specified (ruff, mypy, pytest, rich)

### Missing
- ⚠️ **No configuration files mentioned**: Where are `.ruff.toml`, `mypy.ini`?
- ⚠️ **No CI/CD pipeline**: How are quality gates enforced?
- ⚠️ **No pre-commit hooks**: When do checks run?

### Recommended Additions to plan.md

```markdown
## Constitution Enforcement

### Code Quality Tools (Principle I)

**Configuration Files**:
- `.ruff.toml` - Linting rules (max complexity 10, line length 100)
- `pyproject.toml` - mypy strict mode, black formatting
- `.editorconfig` - Consistent editor settings

**Pre-commit Hooks**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
        args: [--strict]
```

**CI Pipeline** (GitHub Actions):
- Run ruff on every PR
- Run mypy on every PR
- Run pytest with coverage report
- Block merge if coverage <80%

### Testing Standards (Principle II)

**pytest Configuration**:
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=src/pkm
    --cov-report=term-missing
    --cov-fail-under=80
    --strict-markers
```

### Performance Testing (Principle IV)

**Benchmark Setup**:
```python
# tests/benchmarks/test_performance.py
import pytest
from pkm.services import TaskService

@pytest.mark.benchmark
def test_view_tasks_performance(benchmark):
    """Validates SC-003: <500ms for 500 tasks"""
    service = TaskService()
    # Setup 500 tasks
    result = benchmark(service.get_tasks_today)
    assert result.elapsed < 0.5  # 500ms
```
```

---

## Recommendations Summary

### 1. Create tasks.md (CRITICAL - BLOCKING)
**Action**: Run `/speckit.tasks` command to generate implementation task breakdown

**Required Content**:
- Sequential tasks organized by user story
- Exact file paths for each task
- Test-first workflow (write test → implement → verify)
- Dependencies marked explicitly
- Cross-references to spec.md, data-model.md, contracts/

---

### 2. Enhance plan.md with Implementation Roadmap
**Action**: Add "Implementation Roadmap" section with:
- 4 phases (Foundation → Services → CLI → Utilities)
- Dependency tree visualization
- Cross-references to detail documents
- Parallel work opportunities marked

---

### 3. Add Cross-References Throughout
**Action**: Update all documents to link to each other:
- plan.md → data-model.md, contracts/, research.md
- data-model.md → implementation file paths, spec.md requirements
- contracts/ → implementation file paths, test files, spec.md scenarios

---

### 4. Create Test Coverage Map
**Action**: Add "Test Coverage Map" section to plan.md mapping:
- Each user story scenario → specific test function
- Each functional requirement → validating tests
- Each success criterion → performance test

---

### 5. Add Configuration File Checklist
**Action**: Create "Project Setup Checklist" in plan.md:
- [ ] `pyproject.toml` with dependencies
- [ ] `.ruff.toml` with linting rules
- [ ] `mypy.ini` with strict mode
- [ ] `.pre-commit-config.yaml` with hooks
- [ ] `pytest.ini` with coverage settings
- [ ] `.github/workflows/ci.yml` for automated checks

---

## Next Steps

**Immediate**: Run `/speckit.tasks` to generate tasks.md with:
- User story → task mapping
- File-level granularity (which files to create)
- Test-first ordering (tests before implementation)
- Cross-references to all detail documents

**Then**: Enhance plan.md with implementation roadmap and cross-references

**Finally**: Add test coverage map and configuration file specifications
