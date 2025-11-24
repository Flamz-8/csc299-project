"""CLI helper utilities for formatting and display."""

from rich.console import Console
from rich.table import Table

console = Console()


def success(message: str) -> None:
    """Display a success message.

    Args:
        message: Success message to display
    """
    console.print(f"[green]✓[/green] {message}")


def error(message: str) -> None:
    """Display an error message.

    Args:
        message: Error message to display
    """
    console.print(f"[red]✗[/red] {message}", style="red")


def info(message: str) -> None:
    """Display an info message.

    Args:
        message: Info message to display
    """
    console.print(f"[blue]ℹ[/blue] {message}")


def warning(message: str) -> None:
    """Display a warning message.

    Args:
        message: Warning message to display
    """
    console.print(f"[yellow]⚠[/yellow] {message}", style="yellow")


def create_table(title: str, columns: list[str]) -> Table:
    """Create a formatted table.

    Args:
        title: Table title
        columns: Column headers

    Returns:
        Rich Table object
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")
    for col in columns:
        table.add_column(col)
    return table


def format_datetime(dt: object) -> str:
    """Format datetime for display.

    Args:
        dt: Datetime object or string

    Returns:
        Formatted string
    """
    from datetime import datetime

    if dt is None:
        return "-"
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return dt
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M")
    return str(dt)


def truncate(text: str, max_length: int = 50) -> str:
    """Truncate text to max length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
