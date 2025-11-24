"""Main CLI application entry point."""

from pathlib import Path

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def show_onboarding() -> None:
    """Display onboarding message for first-time users."""
    welcome_text = """
# Welcome to Pro Study Planner! 🎓

Your personal knowledge management system for academic success.

## Quick Start - Top 5 Commands

1. **Capture a note**
   ```
   pkm add note "Your note content here"
   ```

2. **Create a task with due date**
   ```
   pkm add task "Submit lab report" --due "tomorrow"
   ```

3. **View your inbox**
   ```
   pkm view inbox
   ```

4. **Organize by course**
   ```
   pkm organize note NOTE_ID --course "Biology 101"
   ```

5. **Search everything**
   ```
   pkm search "keyword"
   ```

## What You Can Do

- **Quick Capture**: Add notes and tasks instantly to your inbox
- **Task Management**: Set due dates, priorities, and break down with subtasks
- **Organization**: Assign items to courses and tag with topics
- **Search**: Find anything across all your notes and tasks
- **Stay on Track**: View tasks due today, this week, or overdue

## Get Help Anytime

- `pkm --help` - See all commands
- `pkm add --help` - Help for add commands
- `pkm help onboarding` - Show this message again

Your data is stored at ~/.pkm/data.json - completely offline and private!

**Tip**: Start by adding a few notes and tasks, then explore organizing them by course.
"""

    md = Markdown(welcome_text)
    panel = Panel(
        md,
        title="[bold cyan]Pro Study Planner[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def check_first_run(data_dir: Path) -> bool:
    """Check if this is the user's first time running the app.

    Args:
        data_dir: Data directory path

    Returns:
        True if first run, False otherwise
    """
    data_file = data_dir / "data.json"
    return not data_file.exists()


@click.group(invoke_without_command=True)
@click.option(
    "--data-dir",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, path_type=str),
    default=None,
    help="Directory for data storage (default: ~/.pkm)",
)
@click.option("--no-color", is_flag=True, help="Disable colored output")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, data_dir: str | None, no_color: bool, verbose: bool) -> None:
    """Pro Study Planner - Terminal-based personal knowledge management for students.

    \b
    Quick capture workflow:
      1. Add notes and tasks to inbox
      2. Organize by course and topic
      3. View filtered lists and search

    \b
    Examples:
      pkm add note "Photosynthesis converts light to energy"
      pkm add task "Submit lab report" --priority high
      pkm view inbox

    \b
    Get help on specific commands:
      pkm add --help
      pkm add note --help
      pkm view --help

    Data is stored at ~/.pkm/data.json (or use --data-dir to customize)
    """
    # Store global options in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["data_dir"] = data_dir
    ctx.obj["no_color"] = no_color
    ctx.obj["verbose"] = verbose

    # Check for first run and show onboarding
    if ctx.invoked_subcommand is None:
        # No subcommand - show help or onboarding
        data_path = Path(data_dir) if data_dir else Path.home() / ".pkm"
        data_path.mkdir(parents=True, exist_ok=True)

        if check_first_run(data_path):
            show_onboarding()
        else:
            # Show help if no subcommand
            click.echo(ctx.get_help())


# Import command groups to register them with the CLI
# This must happen after cli() is defined
from pkm.cli import add, help, note, organize, search, task, view  # noqa: E402, F401


# Add custom error handling for better user experience
@cli.result_callback()
@click.pass_context
def handle_result(ctx: click.Context, result: object, **kwargs: object) -> None:
    """Handle command results and provide helpful error messages."""
    pass  # Results are handled by individual commands


if __name__ == "__main__":
    try:
        cli()
    except click.UsageError as e:
        console.print(f"[red]Error:[/red] {e.message}", style="red")
        console.print("\n[yellow]Tip:[/yellow] Use --help to see available options")
        console.print("Example: pkm add --help")
    except click.ClickException as e:
        e.show()
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}", style="red")
        console.print("[yellow]Please report this issue if it persists.[/yellow]")
