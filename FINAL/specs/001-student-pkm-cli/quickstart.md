# Quickstart Guide: Pro Study Planner

**Phase**: 1 - Design & Contracts  
**Date**: 2025-11-23  
**For**: Implementation Plan `plan.md`

## Overview

Get up and running with the Pro Study Planner in under 5 minutes. This guide covers installation, basic workflows, and common scenarios for students managing class notes and tasks.

---

## Installation

### Prerequisites

- **Python**: 3.11 or higher ([download](https://www.python.org/downloads/))
- **uv**: Modern Python package manager ([install guide](https://github.com/astral-sh/uv))

Check your Python version:
```bash
python --version  # Should show 3.11+
```

### Install uv (if not already installed)

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:
```bash
uv --version
```

### Install Pro Study Planner

**Option 1: From PyPI** (when published):
```bash
uv tool install pro-study-planner
```

**Option 2: From source** (development):
```bash
git clone https://github.com/yourusername/pro-study-planner.git
cd pro-study-planner
uv sync
pkm --version
```

### Verify Installation

```bash
pkm --version
# Output: Pro Study Planner v1.0.0

pkm --help
# Shows available commands
```

---

## First Steps: Quick Capture Workflow

### 1. Capture Your First Note

```bash
# Quick capture to inbox
pkm add note "Need to review chapter 5 for Biology exam"

# Output:
# ✓ Note created: n_20251123_103045_a7c
```

### 2. Create a Task

```bash
# Add a task with due date
pkm add task "Submit lab report" --due "Friday 11:59pm" --priority high

# Output:
# ✓ Task created: t_20251123_140000_xyz
#   Due: Friday, Nov 25 at 11:59 PM (2 days)
#   Priority: high
```

### 3. View Your Inbox

```bash
pkm view inbox

# Output:
# 📥 INBOX (1 note, 1 task)
# 
# NOTES (1)
# ─────────────────────────────────────────
# n_20251123_103045_a7c  Just now
# Need to review chapter 5 for Biology exam
# ─────────────────────────────────────────
# 
# TASKS (1)
# ─────────────────────────────────────────
# t_20251123_140000_xyz  [HIGH] Due Friday, Nov 25
# Submit lab report
# ─────────────────────────────────────────
```

**✅ Success!** You've captured your first note and task.

---

## Organize: Moving to Courses

### Organize the Note

```bash
# Move note from inbox to course
pkm organize note n_20251123_103045_a7c --course "Biology 101"

# Add topics for better categorization
pkm organize note n_20251123_103045_a7c --add-topics "Cell Structure, Exam Prep"

# Output:
# ✓ Note organized: n_20251123_103045_a7c
#   Moved to: Biology 101
#   Added topics: Cell Structure, Exam Prep
```

### Organize the Task

```bash
# Move task to course
pkm organize task t_20251123_140000_xyz --course "Biology 101"

# Output:
# ✓ Task organized: t_20251123_140000_xyz
#   Moved to: Biology 101
```

### View Course Overview

```bash
pkm view course "Biology 101"

# Output:
# 📚 Biology 101 (1 note, 1 task)
# 
# TOPICS
# Cell Structure (1), Exam Prep (1)
# 
# NOTES (1)
# ─────────────────────────────────────────
# n_20251123_103045_a7c  5 min ago · Cell Structure, Exam Prep
# Need to review chapter 5 for Biology exam
# ─────────────────────────────────────────
# 
# TASKS (1 active)
# ─────────────────────────────────────────
# t_20251123_140000_xyz  [HIGH] Due Friday
# Submit lab report
# ─────────────────────────────────────────
```

---

## Common Workflows

### Workflow 1: Lecture Note Capture

**Scenario**: Taking notes during a Biology lecture on photosynthesis.

```bash
# Option A: Quick single-line note
pkm add note "Photosynthesis: 6CO2 + 6H2O → C6H12O6 + 6O2" -c "Biology 101" -t "Photosynthesis"

# Option B: Multi-line note with editor
pkm add note --interactive --course "Biology 101"
# (Opens $EDITOR for long-form content)

# Option C: Quick capture now, organize later
pkm add note "Chloroplast has thylakoid and stroma"
# (Stays in inbox, organize when reviewing)
```

**Best Practice**: Capture fast during lecture, organize during study time.

---

### Workflow 2: Task Management with Subtasks

**Scenario**: Breaking down a large assignment into steps.

```bash
# 1. Create the main task
pkm add task "Complete research paper" -d "Dec 15" -p high -c "English 201"

# Output shows task ID: t_20251123_150000_abc

# 2. Add subtasks
pkm task add-subtask t_20251123_150000_abc "Choose topic"
pkm task add-subtask t_20251123_150000_abc "Find 5 sources"
pkm task add-subtask t_20251123_150000_abc "Write outline"
pkm task add-subtask t_20251123_150000_abc "Draft introduction"
pkm task add-subtask t_20251123_150000_abc "Complete first draft"

# 3. Complete subtasks as you work
pkm task complete-subtask t_20251123_150000_abc 1  # Topic chosen

# Output:
# ✓ Subtask completed: #1
#   Progress: 1/5 subtasks done (20%)

# 4. View progress
pkm view task t_20251123_150000_abc

# Output:
# ✓ Task: t_20251123_150000_abc
# 
# DETAILS
# Title:    Complete research paper
# Due:      Friday, Dec 15 at 11:59 PM (in 22 days)
# Priority: high
# Course:   English 201
# 
# SUBTASKS (1/5 completed)
# ☑ 1. Choose topic
# ☐ 2. Find 5 sources
# ☐ 3. Write outline
# ☐ 4. Draft introduction
# ☐ 5. Complete first draft
```

---

### Workflow 3: Linking Notes to Tasks

**Scenario**: You have notes on photosynthesis and need to reference them for a lab report.

```bash
# 1. Find the note ID
pkm search "photosynthesis"

# Output:
# 🔍 Search results for "photosynthesis" (1 match)
# 
# NOTES (1)
# n_20251120_100000_xyz  Biology 101 · 3 days ago
# Photosynthesis: 6CO2 + 6H2O → C6H12O6 + 6O2

# 2. Link note to task
pkm task link-note t_20251123_150000_abc n_20251120_100000_xyz

# Output:
# ✓ Linked note to task
#   Task: t_20251123_150000_abc - Submit lab report
#   Note: n_20251120_100000_xyz - Photosynthesis notes

# 3. View task to see linked notes
pkm view task t_20251123_150000_abc

# Output includes:
# LINKED NOTES (1)
# n_20251120_100000_xyz  3 days ago
# Photosynthesis: 6CO2 + 6H2O → C6H12O6 + 6O2
```

---

### Workflow 4: Daily Task Review

**Scenario**: Morning routine to see what's due today.

```bash
# View today's tasks
pkm view tasks --filter today

# Output:
# 📋 TASKS (2 due today)
# 
# TODAY (2)
# ─────────────────────────────────────────
# t_123  [HIGH] Due today at 11:59 PM
# Submit lab report
# Biology 101 · 2/3 subtasks done
# 
# t_456  [MEDIUM] Due today at 5:00 PM
# Attend study group
# Math 202
# ─────────────────────────────────────────

# Check this week's tasks
pkm view tasks --filter week

# Check overdue tasks (uh oh!)
pkm view tasks --filter overdue
```

---

### Workflow 5: Search & Discovery

**Scenario**: Preparing for an exam, need to find all notes on a topic.

```bash
# Search across all notes
pkm search "cell structure"

# Output:
# 🔍 Search results for "cell structure" (3 matches)
# 
# NOTES (3)
# n_123  Biology 101 · 2 days ago
# Eukaryotic **cell structure**: nucleus, mitochondria...
# 
# n_456  Biology 101 · 1 week ago
# Prokaryotic vs eukaryotic **cell structure** comparison
# 
# n_789  Biology 101 · 2 weeks ago
# **Cell structure** diagram from textbook

# Narrow search to a specific course
pkm search "structure" --course "Biology 101"

# Search within a topic
pkm search "equation" --topic "Photosynthesis"

# Search only tasks
pkm search "exam" --type tasks
```

---

## Top 5 Commands (By Frequency)

### 1. Quick Capture
```bash
pkm add note "Quick thought or reminder"
pkm add task "Something to do" --due tomorrow
```

### 2. View Inbox
```bash
pkm view inbox
```

### 3. View Today's Tasks
```bash
pkm view tasks --filter today
```

### 4. Organize Item
```bash
pkm organize note {id} --course "Course Name"
pkm organize task {id} --course "Course Name"
```

### 5. Search
```bash
pkm search "keyword"
```

**💡 Tip**: Set up shell aliases for frequent commands:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias pn='pkm add note'
alias pt='pkm add task'
alias pi='pkm view inbox'
alias ptd='pkm view tasks --filter today'
```

---

## Sample Data Walkthrough

Let's simulate a student's typical week:

### Monday: Capture Phase

```bash
# During Biology lecture
pkm add note "Mitochondria: powerhouse of the cell" -c "Biology 101" -t "Cell Structure"
pkm add note "Quiz next Friday on chapters 3-5" -c "Biology 101"

# During Math class
pkm add note "Derivative chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x)" -c "Calculus 201" -t "Derivatives"

# After classes
pkm add task "Study for Bio quiz" -d "Friday" -p high -c "Biology 101"
pkm add task "Finish problem set 3" -d "Wednesday" -c "Calculus 201"
```

### Wednesday: Organize Phase

```bash
# Review inbox (should be empty if capturing with --course)
pkm view inbox

# View course progress
pkm view course "Biology 101"
pkm view course "Calculus 201"

# Complete tasks
pkm task complete {math_task_id}
```

### Friday: Search & Review

```bash
# Preparing for quiz - find all relevant notes
pkm search "chapter" --course "Biology 101"

# Check what's due
pkm view tasks --filter today

# Mark quiz task complete after taking it
pkm task complete {bio_quiz_task_id}
```

---

## Advanced Tips

### Tip 1: Multi-line Notes

Use quotes and newlines:
```bash
pkm add note "First line
Second line
Third line" -c "Course"
```

Or use interactive mode:
```bash
pkm add note --interactive
# Opens $EDITOR (vim, nano, VS Code, etc.)
```

### Tip 2: Natural Language Dates

```bash
pkm add task "Review notes" --due tomorrow
pkm add task "Start project" --due "next Monday"
pkm add task "Submit paper" --due "Dec 15 at 11:59pm"
pkm add task "Office hours" --due "2025-12-01"
```

### Tip 3: Batch Organization

```bash
# Organize multiple items by viewing inbox first
pkm view inbox

# Then organize each:
pkm organize note n_123 -c "Biology 101"
pkm organize note n_456 -c "Biology 101"
pkm organize task t_789 -c "Math 202"
```

### Tip 4: Topic Hygiene

Keep topics consistent (avoid synonyms):
```bash
# Good: Consistent naming
-t "Cell Structure"
-t "Cell Structure"

# Bad: Synonyms fragment your topics
-t "Cell Structure"
-t "Cells"
-t "Cellular Structure"
```

### Tip 5: Backup Your Data

Data is stored in `~/.pkm/data.json`. Back it up regularly:

**macOS/Linux**:
```bash
cp ~/.pkm/data.json ~/Dropbox/pkm-backup-$(date +%Y%m%d).json
```

**Windows**:
```powershell
Copy-Item ~/.pkm/data.json ~/Dropbox/pkm-backup-$(Get-Date -Format 'yyyyMMdd').json
```

Or use version control:
```bash
cd ~/.pkm
git init
git add data.json
git commit -m "Backup $(date)"
```

---

## Troubleshooting

### Issue: Command not found

**Solution**: Ensure `pkm` is in your PATH.

**uv tool install** (recommended):
```bash
uv tool install student-pkm
# Adds to PATH automatically
```

**From source**:
```bash
uv run pkm  # Prefix with 'uv run'
# Or activate virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pkm --version
```

### Issue: Permission denied on data.json

**Solution**: Check file permissions.

```bash
ls -la ~/.pkm/data.json
chmod 644 ~/.pkm/data.json
```

### Issue: Date parsing fails

**Examples**:
```bash
# ✗ "friday" (lowercase, ambiguous)
# ✓ "Friday" or "next Friday"

# ✗ "12/1" (ambiguous format)
# ✓ "Dec 1" or "2025-12-01"

# ✗ "11:59" (no date)
# ✓ "Friday 11:59pm"
```

### Issue: Note/task not found

**Solution**: Double-check ID format.

```bash
# IDs are case-sensitive and exact:
pkm view note n_20251123_103045_a7c  # ✓
pkm view note n_20251123             # ✗ (partial ID)
```

Use search to find items:
```bash
pkm search "partial content"
```

---

## Next Steps

### Learn More

- **Data Model**: See `data-model.md` for entity schemas and relationships
- **CLI Reference**: See `contracts/cli-interface.md` for all commands and options
- **Implementation Plan**: See `plan.md` for architecture and technical decisions

### Customize

1. **Set default course**: Add to shell profile
   ```bash
   export PKM_DEFAULT_COURSE="Biology 101"
   ```

2. **Change data directory**:
   ```bash
   pkm --data-dir ~/custom/path view inbox
   ```

3. **Disable colors** (for scripting):
   ```bash
   pkm --no-color view tasks > tasks.txt
   ```

### Integrate with Other Tools

- **Export to Markdown**: Future feature
- **Sync with Notion/Obsidian**: Future feature
- **Calendar integration**: Future feature

---

## Summary

**Installation**: `uv tool install pro-study-planner` → `pkm --version`

**Core Workflow**:
1. **Capture**: `pkm add note` / `pkm add task`
2. **View**: `pkm view inbox` / `pkm view tasks`
3. **Organize**: `pkm organize note/task {id} --course`
4. **Search**: `pkm search "keyword"`
5. **Complete**: `pkm task complete {id}`

**Performance**: All commands < 1 second (per Constitution Check).

**Data Location**: `~/.pkm/data.json` (backup regularly!)

**Get Help**: `pkm help [command]` or `pkm --help`

---

**Ready to boost your productivity?** Start with `pkm add note "First note!"` 🚀
