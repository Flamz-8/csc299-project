# Feature Specification: Pro Study Planner

**Feature Branch**: `001-student-pkm-cli`  
**Created**: 2025-11-23  
**Status**: Draft  
**Input**: User description: "Build a terminal-based personal knowledge management (PKM) app for students that helps them capture class notes and manage tasks/todos in one place"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Quick Capture (Priority: P1)

Students can rapidly capture notes and tasks into an "inbox" with minimal fields, then organize them later when they have time. This addresses the core problem: stressed students need to capture information fast during or between classes without breaking flow.

**Why this priority**: This is the foundation of the entire system. If students can't quickly capture information with minimal friction, they won't use the tool at all. Every other feature depends on having data in the system.

**Independent Test**: Can be fully tested by launching the app, adding 3 inbox notes and 2 inbox tasks with single commands, then viewing the inbox list. Delivers immediate value as a simple scratch pad.

**Acceptance Scenarios**:

1. **Given** the CLI is running, **When** user runs `add note "Chapter 5 photosynthesis examples"`, **Then** a new note is created in the inbox with a timestamp and unique ID
2. **Given** the CLI is running, **When** user runs `add task "Finish math homework"`, **Then** a new task is created in the inbox with a timestamp, unique ID, and no due date
3. **Given** there are 5 items in the inbox, **When** user runs `view inbox`, **Then** all 5 items are displayed with IDs, timestamps, and content
4. **Given** the user wants minimal typing, **When** user runs `add "Quick thought"`, **Then** the system prompts whether this is a note or task, then creates it in the inbox

---

### User Story 2 - Task Management with Due Dates (Priority: P1)

Students can create tasks with due dates and view filtered lists (today, this week, overdue) to understand what needs attention now. This solves the "what should I work on?" problem that overwhelms students.

**Why this priority**: Knowing what's due today/this week is critical for student success. This is the primary motivator for using a task system and must work alongside quick capture.

**Independent Test**: Can be fully tested by creating 5 tasks with different due dates (today, tomorrow, next week, past due), then viewing filtered lists. Delivers value as a simple task tracker even without notes.

**Acceptance Scenarios**:

1. **Given** the user is in the main menu, **When** user runs `add task "Submit lab report" --due 2025-11-25`, **Then** a task is created with the specified due date
2. **Given** today is 2025-11-23 and there are tasks due today, tomorrow, and next week, **When** user runs `view today`, **Then** only tasks due today are displayed
3. **Given** today is 2025-11-23 and there are tasks due on 2025-11-24, 2025-11-26, and 2025-11-30, **When** user runs `view week`, **Then** all tasks due within 7 days from today are displayed
4. **Given** today is 2025-11-23 and there are tasks due on 2025-11-20 and 2025-11-21, **When** user runs `view overdue`, **Then** only tasks with due dates before today are displayed, sorted by oldest first
5. **Given** a task exists, **When** user runs `task 123 done`, **Then** the task is marked complete and removed from active views

---

### User Story 3 - Organize by Course (Priority: P2)

Students can assign notes and tasks to courses, then view everything related to a specific class. This helps compartmentalize work and review course-specific information.

**Why this priority**: Students juggle multiple classes; organization by course is essential for mental clarity. This builds on P1 stories by adding structure to captured data.

**Independent Test**: Can be fully tested by creating 2 courses, adding 3 notes and 2 tasks to each course, then viewing filtered lists by course. Delivers organizational value independently.

**Acceptance Scenarios**:

1. **Given** the user has inbox items, **When** user runs `organize note 456 --course "Biology 101"`, **Then** the note is moved from inbox to the Biology 101 course
2. **Given** the user is creating a new task, **When** user runs `add task "Read chapter 3" --course "History 201" --due 2025-11-25`, **Then** the task is created directly in the History 201 course, not in inbox
3. **Given** there are notes and tasks in multiple courses, **When** user runs `view course "Biology 101"`, **Then** all notes and tasks for Biology 101 are displayed together
4. **Given** there are tasks across multiple courses, **When** user runs `view tasks --course "Math 301"`, **Then** only tasks assigned to Math 301 are displayed
5. **Given** a user wants to see all courses, **When** user runs `list courses`, **Then** all course names are displayed with item counts (notes and tasks per course)

---

### User Story 4 - Note Organization and Viewing (Priority: P2)

Students can organize notes by topic within courses, edit existing notes, and view notes in structured lists. This creates a lightweight knowledge base for studying.

**Why this priority**: Notes are only valuable if students can find and review them. Organization by topic creates study-friendly structure. Must come after basic capture and course organization.

**Independent Test**: Can be fully tested by creating a course, adding 4 notes with different topics, editing one note, and viewing filtered lists. Works independently as a simple note-taking system.

**Acceptance Scenarios**:

1. **Given** a note exists in a course, **When** user runs `organize note 789 --topic "Cell Structure"`, **Then** the note is tagged with the topic "Cell Structure"
2. **Given** a note exists, **When** user runs `edit note 789`, **Then** the note content opens in the user's default text editor (determined by $EDITOR or system default)
3. **Given** there are notes in Biology 101 with topics "Cell Structure" and "Photosynthesis", **When** user runs `view notes --course "Biology 101" --topic "Cell Structure"`, **Then** only notes matching both filters are displayed
4. **Given** there are multiple notes, **When** user runs `view notes`, **Then** all notes are displayed grouped by course, then by topic, with timestamps
5. **Given** a note is no longer needed, **When** user runs `delete note 789`, **Then** the note is removed after confirmation prompt

---

### User Story 5 - Search Across Everything (Priority: P3)

Students can search all notes and tasks by keyword, course, or tag to quickly find specific information. This supports studying and finding forgotten tasks.

**Why this priority**: As data accumulates, search becomes essential. However, students can manually browse in early usage, so this is less critical than core capture/organization features.

**Independent Test**: Can be fully tested by populating the system with 20 notes and 15 tasks across 3 courses, then searching by various keywords and filters. Delivers value as a productivity multiplier.

**Acceptance Scenarios**:

1. **Given** there are notes and tasks containing the word "photosynthesis", **When** user runs `search "photosynthesis"`, **Then** all matching notes and tasks are displayed with highlighted matches
2. **Given** there are items across multiple courses, **When** user runs `search "exam" --course "Biology 101"`, **Then** only items from Biology 101 containing "exam" are displayed
3. **Given** notes have topics tagged, **When** user runs `search --topic "Cell Structure"`, **Then** all notes tagged with that topic are displayed
4. **Given** a search returns many results, **When** user runs `search "homework" --type task`, **Then** only tasks (not notes) containing "homework" are displayed
5. **Given** a search returns zero results, **When** user runs `search "nonexistent"`, **Then** a friendly message indicates no matches found and suggests checking spelling

---

### User Story 6 - Link Notes to Tasks (Priority: P3)

Students can reference specific notes from tasks, creating connections between "what to do" and "information needed to do it". This reduces cognitive load when working on assignments.

**Why this priority**: Linking notes to tasks is valuable but not essential for basic functionality. Students can manually remember which notes relate to which tasks until the system has substantial data.

**Independent Test**: Can be fully tested by creating 3 notes and 2 tasks, linking notes to tasks, then viewing task details that show linked notes. Delivers value as a context enhancer.

**Acceptance Scenarios**:

1. **Given** a task and a note both exist, **When** user runs `task 123 link note 456`, **Then** the note is associated with the task
2. **Given** a task has 2 linked notes, **When** user runs `view task 123`, **Then** task details are displayed including a list of linked note IDs and their titles
3. **Given** a task has linked notes, **When** user runs `view task 123 --expand`, **Then** task details and full content of all linked notes are displayed
4. **Given** a task has a linked note, **When** user runs `task 123 unlink note 456`, **Then** the link is removed
5. **Given** a note is linked to multiple tasks, **When** user runs `view note 456`, **Then** note details include a list of tasks that reference this note

---

### User Story 7 - Task Priority and Subtasks (Priority: P3)

Students can assign priority levels to tasks (high, medium, low) and break down complex tasks into subtasks. This helps with planning and reduces overwhelm on large assignments.

**Why this priority**: Priority and subtasks are helpful for advanced task management, but not essential for initial adoption. Basic task lists with due dates handle most student needs.

**Independent Test**: Can be fully tested by creating a task with high priority and 3 subtasks, completing subtasks one by one, and viewing priority-filtered lists. Works independently as enhanced task management.

**Acceptance Scenarios**:

1. **Given** a task is being created, **When** user runs `add task "Study for final exam" --priority high --due 2025-12-15`, **Then** the task is created with high priority
2. **Given** a task exists, **When** user runs `task 123 add-subtask "Review chapter 1"`, **Then** a subtask is added to the task
3. **Given** a task has 3 subtasks with 1 completed, **When** user runs `view task 123`, **Then** task details show progress (1/3 subtasks completed)
4. **Given** a subtask exists, **When** user runs `task 123 subtask 1 done`, **Then** the subtask is marked complete
5. **Given** there are tasks with different priorities, **When** user runs `view tasks --priority high`, **Then** only high-priority tasks are displayed, sorted by due date
6. **Given** a task has all subtasks completed, **When** viewing the task, **Then** the system suggests marking the parent task complete

---

### User Story 8 - Onboarding and Help (Priority: P2)

Students can run a help command that lists main commands, view command-specific help, and get a guided first-run experience. This reduces friction for new users.

**Why this priority**: Good help is essential for adoption, especially for stressed students who won't read external docs. This should be available early but isn't needed until basic commands exist.

**Independent Test**: Can be fully tested by running the app for the first time, going through onboarding, then accessing help for specific commands. Delivers value as a learning aid.

**Acceptance Scenarios**:

1. **Given** the user runs the app for the first time, **When** the CLI launches, **Then** a welcome message explains the concept and shows top 5 commands to get started
2. **Given** the user is in the app, **When** user runs `help`, **Then** a list of all available commands with brief descriptions is displayed
3. **Given** the user needs command-specific help, **When** user runs `help add`, **Then** detailed help for the `add` command is displayed with examples and all options
4. **Given** the user types an invalid command, **When** user runs `invalidcommand`, **Then** an error message suggests similar valid commands and points to `help`
5. **Given** the user wants to review onboarding, **When** user runs `help onboarding`, **Then** the first-run tutorial is displayed again

---

### Edge Cases

- What happens when a user tries to add a task with a past due date? (System should allow it and immediately show it in "overdue" view)
- What happens when a user tries to organize an item to a course that doesn't exist yet? (System should auto-create the course or prompt to create it)
- What happens when the data file is corrupted or missing? (System should detect corruption, backup the file, and start fresh with error message)
- What happens when a user tries to delete a note that's linked to tasks? (System should warn about linked tasks and ask for confirmation before deleting)
- What happens when searching with no items in the system? (System should show a friendly message suggesting they add some notes/tasks first)
- What happens when a user provides an invalid date format? (System should show the expected format and examples of valid dates)
- What happens when two tasks have the same due date? (System should display them sorted by creation time or priority)
- What happens when the terminal window is too small to display task lists? (System should handle text wrapping gracefully or paginate results)
- What happens when a user tries to edit a non-existent note ID? (System should show clear error message with available note IDs)
- What happens when the user's $EDITOR environment variable is not set? (System should fall back to a sensible default like nano, vim, or notepad depending on OS)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST run entirely in the terminal (CLI only) with no graphical interface dependencies
- **FR-002**: System MUST support cross-platform operation on Linux, macOS, and Windows terminals with minimal setup
- **FR-003**: Users MUST be able to create notes with content, timestamp, and optional course/topic metadata
- **FR-004**: Users MUST be able to create tasks with title, optional due date, optional priority (high/medium/low), and optional course assignment
- **FR-005**: System MUST provide an "inbox" for quickly captured items that haven't been organized yet
- **FR-006**: Users MUST be able to assign both notes and tasks to courses for organizational grouping
- **FR-007**: Users MUST be able to tag notes with topics for finer-grained organization within courses
- **FR-008**: System MUST allow users to link one or more notes to a task to provide context
- **FR-009**: Users MUST be able to create subtasks under a parent task for complex assignments
- **FR-010**: System MUST provide filtered task views: today, this week, overdue, all tasks by course
- **FR-011**: Users MUST be able to mark tasks and subtasks as complete
- **FR-012**: System MUST support searching notes and tasks by keyword, course, topic, or type
- **FR-013**: Users MUST be able to edit existing notes using their preferred text editor
- **FR-014**: Users MUST be able to delete notes and tasks with confirmation prompts
- **FR-015**: System MUST store all data locally in human-readable files (JSON or plain text format)
- **FR-016**: System MUST operate completely offline with no external service dependencies
- **FR-017**: System MUST provide a help command that lists all available commands with descriptions
- **FR-018**: System MUST provide command-specific help with usage examples
- **FR-019**: System MUST display a first-run onboarding experience explaining core commands
- **FR-020**: System MUST handle invalid commands gracefully with helpful error messages and suggestions
- **FR-021**: System MUST validate date inputs and provide clear error messages for invalid formats
- **FR-022**: System MUST generate unique IDs for all notes and tasks to enable unambiguous references
- **FR-023**: System MUST display timestamps in human-readable format (e.g., "2 hours ago", "Nov 23, 2025")
- **FR-024**: System MUST handle corrupted data files by creating backups and allowing fresh starts
- **FR-025**: System MUST respect the user's $EDITOR environment variable or fall back to sensible defaults per platform

### Key Entities

- **Note**: A piece of information captured by a student. Attributes include unique ID, content/body text, creation timestamp, last modified timestamp, optional course assignment, optional topic tags, and list of tasks that link to this note.

- **Task**: An actionable item with a deadline. Attributes include unique ID, title/description, creation timestamp, due date (optional), priority level (high/medium/low, default medium), completion status (boolean), optional course assignment, list of linked note IDs, and list of subtasks.

- **Subtask**: A smaller actionable item nested under a parent task. Attributes include unique ID (scoped to parent task), title/description, completion status, and creation timestamp.

- **Course**: An organizational container representing a class/subject. Attributes include unique name/identifier, creation timestamp, and counts of associated notes and tasks.

- **Topic**: A tag for categorizing notes within a course. Attributes include name/label and optional course association (topics may be course-specific or global).

- **Inbox**: A virtual container for uncategorized notes and tasks. Items in the inbox have no course assignment and are meant for later organization.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can capture a note or task from the command line in under 5 seconds (single command execution)
- **SC-002**: The app launches and displays the main menu or command prompt in under 1 second on typical student hardware
- **SC-003**: Viewing filtered task lists (today, week, overdue) completes in under 500ms for datasets up to 500 tasks
- **SC-004**: Search operations return results in under 1 second for datasets containing up to 1,000 notes and 500 tasks
- **SC-005**: First-time users can complete onboarding and create their first note/task within 2 minutes
- **SC-006**: The help system provides relevant command information within 2 commands (e.g., `help` → `help add`)
- **SC-007**: Data files remain human-readable and can be backed up/versioned with standard file tools
- **SC-008**: The app runs on Linux, macOS, and Windows without requiring platform-specific installations beyond a runtime (e.g., Python, Node.js)
- **SC-009**: Error messages provide actionable guidance that allows students to self-correct 90% of common mistakes
- **SC-010**: Students can organize 10 inbox items into courses and topics in under 3 minutes using batch commands or workflows
- **SC-011**: Task completion rate improves by enabling students to see "what's due today" in a single command execution
- **SC-012**: System operates reliably offline with zero cloud dependencies, eliminating internet connectivity as a blocker

## Assumptions *(mandatory)*

- Students have basic terminal/command-line familiarity (can navigate directories, run commands)
- Students have a terminal emulator installed (default on Linux/macOS, PowerShell/CMD on Windows)
- Students will install a single runtime dependency (e.g., Python 3.x, Node.js) if needed for the implementation
- Students prefer keyboard-driven workflows over mouse interaction when working in the terminal
- Students' typical dataset size: 10-20 courses per semester, 50-200 notes total, 20-100 active tasks
- Students will use the app daily or multiple times per week during academic terms
- Students value speed and minimal friction over rich formatting or visual polish
- Students have access to a text editor (nano, vim, notepad, VS Code) for editing note content
- Data persistence requirements are satisfied by local file storage; cloud sync is explicitly out of scope
- A single student uses the system on a single machine (no multi-user collaboration)

## Out of Scope *(mandatory)*

- Graphical user interface (GUI) or web interface
- Cloud synchronization or multi-device sync
- Collaboration features (sharing notes/tasks with other students)
- Rich text formatting, images, or embedded media in notes
- Calendar integration or external app synchronization
- Mobile app versions (iOS, Android)
- Advanced analytics, productivity metrics, or time tracking
- Reminders, notifications, or background processes
- Export to PDF, Word, or other formatted document types
- Plugin system or third-party extensions
- User authentication or multi-user support
- Network features or API endpoints
- Integration with learning management systems (Canvas, Blackboard, etc.)
- Spaced repetition or flashcard features for studying
- Grade tracking or GPA calculation
- Attachment handling for files/documents

## Dependencies & Constraints *(mandatory)*

### Dependencies

- A scripting/programming language runtime suitable for CLI development (e.g., Python 3.8+, Node.js 14+, or similar)
- Standard library support for file I/O, JSON parsing, and date/time handling
- Access to environment variables for editor detection ($EDITOR, %EDITOR%)
- Terminal emulator with standard input/output streams (stdin, stdout, stderr)

### Constraints

- **Platform Compatibility**: Must work identically on Linux, macOS, and Windows (handle path separators, line endings, default editors)
- **No External Services**: Zero network calls; completely offline operation
- **Human-Readable Storage**: Data files must be editable with a text editor (JSON preferred over binary formats)
- **Minimal Setup**: Installation must not require complex build processes or multiple dependency installations
- **Terminal Limitations**: Must handle varying terminal window sizes gracefully (no assumptions about 80x24 or larger)
- **Performance**: All operations must feel instant (<1s) for typical student datasets (500 notes, 200 tasks)
- **Data Safety**: Must not lose data on crashes; write operations should be atomic or have corruption recovery
- **Accessibility**: Terminal-based means it works with screen readers that support terminal applications

## Notes

- The primary design philosophy is "quick capture, organize later" to match student cognitive load patterns
- Command syntax should be intuitive and forgiving (accept variations, suggest corrections for typos)
- Consider a REPL-style interface (interactive shell) vs pure command-line arguments based on user testing
- Default date parsing should handle natural language where feasible ("tomorrow", "next friday", "12/15")
- The inbox concept is critical to adoption; many students will use it as the primary interface initially
- Consider providing example data or a "demo mode" to help students understand the system quickly
- Data file location should be configurable via environment variable or config file for backup flexibility
- Future enhancement potential: export to markdown, integration with git for versioning notes, sync via git repos
