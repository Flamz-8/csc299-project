# Quick Start Guide: Task Management CLI

**Welcome!** 🎉 This guide will help you get started with the task management CLI in just a few minutes.

## What is this?

A simple, fast command-line tool for managing your tasks. Add tasks, view your list, and keep track of what needs to be done—all from your terminal.

## Installation

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv (if you don't have it)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

### Install tasks CLI

```bash
# Clone the repository
git clone <repository-url>
cd task5

# Install the project
uv pip install -e .

# Verify installation
tasks --help
```

## Basic Usage

### Adding Your First Task

```bash
tasks add "Buy groceries"
```

**Output:**
```
Task added: [1] Buy groceries
```

Each task gets a unique ID (the number in brackets) that you can use for future operations.

### Adding More Tasks

```bash
tasks add "Write project documentation"
tasks add "Call dentist for appointment"
tasks add "Review pull requests"
```

### Viewing All Tasks

```bash
tasks list
```

**Output:**
```
[1] Buy groceries
[3] Call dentist for appointment
[2] Review pull requests
[4] Write project documentation
```

**Note:** Tasks are displayed in alphabetical order (case-insensitive) for easy scanning.

### When You Have No Tasks

```bash
tasks list
```

**Output:**
```
No tasks found
```

## Examples

### Real-World Task Management

```bash
# Morning planning
tasks add "Respond to emails"
tasks add "Team standup at 10am"
tasks add "Finish quarterly report"

# Check what's on your plate
tasks list
# [2] Finish quarterly report
# [1] Respond to emails
# [3] Team standup at 10am

# Add more as they come up
tasks add "Book flight for conference"
tasks add "Review budget proposal"

# See updated list
tasks list
# [4] Book flight for conference
# [2] Finish quarterly report
# [1] Respond to emails
# [5] Review budget proposal
# [3] Team standup at 10am
```

### Task Descriptions

You can use natural language and include details:

```bash
tasks add "Buy groceries: milk, eggs, bread, coffee"
tasks add "Meeting with Sarah at 3pm (Conference Room B)"
tasks add "Debug issue #42 - login form validation"
```

### Special Characters

Tasks can include most characters, but remember to quote them:

```bash
# Good (quoted)
tasks add "Review John's code"
tasks add "Buy 2-3 items at store"
tasks add "Task with emoji 🎯"

# Won't work (not quoted)
tasks add Review John's code  # Error: unrecognized arguments
```

## Where Are My Tasks Stored?

Your tasks are stored in a JSON file in your home directory:

- **macOS/Linux**: `~/.tasks.json`
- **Windows**: `C:\Users\YourName\.tasks.json`

You can view or edit this file directly if needed (it's human-readable), but the CLI is the recommended way to interact with your tasks.

## Common Questions

### Can I add an empty task?

No, task descriptions must have at least one character:

```bash
tasks add ""
# Error: Task description cannot be empty
```

### How long can task descriptions be?

Up to 1,000 characters. Most tasks will be much shorter, but you have room for detailed descriptions if needed.

### What if I make a typo?

In this MVP version, you can't edit or delete tasks yet. These features are planned for future releases. For now, you can manually edit the `~/.tasks.json` file if needed.

### Do tasks persist between sessions?

Yes! Your tasks are saved to disk and will be available every time you run `tasks list`, even after rebooting your computer.

### Can I use this with multiple people?

The current version is designed for single-user, local use. Each person would have their own task list in their home directory.

## Troubleshooting

### "command not found: tasks"

**Problem:** The `tasks` command isn't in your PATH.

**Solution:**
```bash
# Make sure you installed with -e flag
uv pip install -e .

# Or run directly using Python module
python -m tasks_cli list
```

### "Error: Tasks file is corrupted"

**Problem:** The JSON file has been manually edited incorrectly or was corrupted.

**Solution:** The CLI automatically backs up corrupted files to `~/.tasks.json.backup` and starts fresh. You can manually recover data from the backup file if needed.

### Permission errors

**Problem:** Can't read or write the tasks file.

**Solution:** Check file permissions on `~/.tasks.json`. The file should be readable and writable by your user account.

## Advanced Usage

### Using a Different Storage Location

You can override the default storage location with an environment variable:

```bash
# Use a custom location
export TASKS_FILE=~/Documents/my-tasks.json
tasks add "This goes to custom location"
tasks list

# Just for one command (Linux/macOS)
TASKS_FILE=/tmp/test-tasks.json tasks list

# Just for one command (Windows PowerShell)
$env:TASKS_FILE="C:\temp\test-tasks.json"; tasks list
```

This is useful for:
- Testing
- Having separate task lists for different projects
- Storing tasks in a synced folder (Dropbox, iCloud, etc.)

## What's Next?

This is the Minimum Viable Product (MVP) with core functionality. Future versions will include:

- ✨ **Task completion**: Mark tasks as done
- ✨ **Task editing**: Fix typos and update descriptions
- ✨ **Task deletion**: Remove tasks you no longer need
- ✨ **Search/filter**: Find specific tasks quickly
- ✨ **Priorities**: Mark tasks as high/low priority
- ✨ **Due dates**: Track when tasks are due
- ✨ **Categories/tags**: Organize tasks by project or context

## Getting Help

```bash
# See all available commands
tasks --help

# Get help for a specific command
tasks add --help
tasks list --help
```

## Examples Cheat Sheet

```bash
# Add tasks
tasks add "Buy groceries"
tasks add "Important meeting at 2pm"
tasks add "Review code for pull request #123"

# View all tasks
tasks list

# Custom storage location
export TASKS_FILE=~/my-project-tasks.json
tasks add "Project-specific task"
```

---

**Happy task managing!** 🚀

If you encounter any issues or have suggestions, please open an issue in the project repository.
