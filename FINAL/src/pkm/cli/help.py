"""Help and onboarding commands."""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from pkm.cli.main import cli, show_onboarding

console = Console()


@cli.group()
def help_cmd() -> None:
    """Get help with Pro Study Planner commands.

    \b
    Commands:
      pkm help onboarding  - Show welcome tutorial again
      pkm help commands    - List all available commands
    """
    pass


@help_cmd.command(name="onboarding")
def help_onboarding() -> None:
    """Display the onboarding tutorial.

    Shows the welcome message with quick start guide and top commands.
    Useful for new users or as a refresher.

    \b
    Example:
      pkm help onboarding
    """
    show_onboarding()


@help_cmd.command(name="commands")
@click.pass_context
def help_commands(ctx: click.Context) -> None:
    """List all available commands with brief descriptions.

    \b
    Example:
      pkm help commands
    """
    commands_text = """
# Pro Study Planner - Command Reference

## Adding Items
- `pkm add note CONTENT` - Add a note to inbox
- `pkm add task TITLE` - Add a task to inbox

## Viewing Data
- `pkm view inbox` - Show unorganized notes and tasks
- `pkm view today` - Tasks due today
- `pkm view week` - Tasks due this week
- `pkm view overdue` - Past-due tasks
- `pkm view courses` - List all courses
- `pkm view course NAME` - View items in a course

## Organizing
- `pkm organize note ID --course NAME` - Assign note to course
- `pkm organize task ID --course NAME` - Assign task to course

## Task Management
- `pkm task complete ID` - Mark task as done
- `pkm task add-subtask ID TITLE` - Add a subtask
- `pkm task check-subtask ID NUM` - Complete a subtask

## Note Management
- `pkm note edit ID` - Edit note in external editor
- `pkm note delete ID` - Delete a note
- `pkm note add-topic ID TOPIC` - Add topic to note
- `pkm note remove-topic ID TOPIC` - Remove topic from note

## Search
- `pkm search QUERY` - Search notes and tasks
- `pkm search QUERY --type notes` - Search only notes
- `pkm search QUERY --course NAME` - Search within course

## Help
- `pkm --help` - Show general help
- `pkm COMMAND --help` - Help for specific command
- `pkm help onboarding` - Show tutorial again

## Tips
- Use quotes for multi-word arguments: `"Biology 101"`
- Add `-h` or `--help` to any command for details
- Natural language dates work: `--due "tomorrow"`
- Chain options: `--priority high --due "next Friday"`
"""

    md = Markdown(commands_text)
    panel = Panel(
        md,
        title="[bold cyan]Command Reference[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)
