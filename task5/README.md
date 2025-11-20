# Task Management CLI

A simple, fast command-line tool for managing your tasks. Add tasks, view your list, and keep track of what needs to be done—all from your terminal.

## Features

- ✅ Add tasks with simple commands
- ✅ List all tasks in alphabetical order
- ✅ Persistent storage in JSON format
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Fast and lightweight (<50MB memory)

## Installation

### Prerequisites

- Python 3.13 or higher
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

# Install in development mode
uv pip install -e .

# Verify installation
tasks --help
```

## Usage

### Adding Tasks

```bash
tasks add "Buy groceries"
tasks add "Write project documentation"
tasks add "Call dentist for appointment"
```

**Output:**
```
Task added: [1] Buy groceries
Task added: [2] Write project documentation
Task added: [3] Call dentist for appointment
```

### Listing Tasks

```bash
tasks list
```

**Output:**
```
[1] Buy groceries
[3] Call dentist for appointment
[2] Write project documentation
```

**Note:** Tasks are displayed in alphabetical order (case-insensitive) for easy scanning.

### Empty List

```bash
tasks list
```

**Output:**
```
No tasks found
```

## Examples

### Daily Task Management

```bash
# Morning planning
tasks add "Respond to emails"
tasks add "Team standup at 10am"
tasks add "Finish quarterly report"

# Check your tasks
tasks list
# [2] Finish quarterly report
# [1] Respond to emails
# [3] Team standup at 10am

# Add tasks throughout the day
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

### Task Descriptions with Details

```bash
tasks add "Buy groceries: milk, eggs, bread, coffee"
tasks add "Meeting with Sarah at 3pm (Conference Room B)"
tasks add "Debug issue #42 - login form validation"
```

### Using Special Characters

Remember to quote task descriptions:

```bash
# ✅ Good (quoted)
tasks add "Review John's code"
tasks add "Buy 2-3 items at store"

# ❌ Won't work (not quoted)
tasks add Review John's code  # Error
```

## Storage

Your tasks are stored in a JSON file in your home directory:

- **macOS/Linux**: `~/.tasks.json`
- **Windows**: `C:\Users\YourName\.tasks.json`

The file is human-readable and can be manually edited if needed, though using the CLI is recommended.

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

### "Error: Task description cannot be empty"

**Problem:** Attempting to add a task without a description.

**Solution:**
```bash
# Provide a description
tasks add "Your task description here"
```

### "Error: Cannot write tasks file"

**Problem:** Permission issues or disk full.

**Solution:**
- Check file permissions on your home directory
- Ensure you have disk space available
- On Windows, try running as Administrator if needed

### "Error: Tasks file is corrupted"

**Problem:** The JSON file was manually edited incorrectly or corrupted.

**Solution:** The CLI automatically backs up corrupted files to `~/.tasks.json.backup` and starts with an empty list. You can manually recover data from the backup if needed:

```bash
# View the backup
cat ~/.tasks.json.backup  # macOS/Linux
Get-Content ~\.tasks.json.backup  # Windows PowerShell

# Manually fix and restore if possible
```

## Development

### Running Tests

```bash
# Run all tests with coverage
uv run pytest --cov=src/tasks_cli --cov-report=term-missing

# Run specific test types
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/contract/
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Type checking
uv run mypy src/

# Formatting
uv run black .
```

## Technical Details

- **Language**: Python 3.13+
- **Storage Format**: JSON (human-readable)
- **Performance**: Add <100ms, List <200ms (typical usage)
- **Memory**: <50MB footprint
- **Architecture**: Clear separation between CLI and storage layers

## Future Enhancements

Planned features for future releases:

- Task deletion
- Task editing
- Mark tasks as complete
- Task search and filtering
- Task priorities
- Due dates and reminders
- Import/export functionality

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
