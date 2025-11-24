"""Add commands for creating notes and tasks."""

from pathlib import Path

import click

from pkm.cli.helpers import error, info, success
from pkm.cli.main import cli
from pkm.services.note_service import NoteService
from pkm.services.task_service import TaskService
from pkm.utils.date_parser import format_due_date, parse_due_date


def get_data_dir(ctx: click.Context) -> Path:
    """Get data directory from context or use default.

    Args:
        ctx: Click context

    Returns:
        Path to data directory
    """
    data_dir = ctx.obj.get("data_dir")
    if data_dir is None:
        data_dir = Path.home() / ".pkm"
    else:
        data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


@cli.group()
def add() -> None:
    """Add notes and tasks to your inbox.

    \b
    Quick capture commands:
      pkm add note CONTENT   - Capture a note
      pkm add task TITLE     - Create a task

    \b
    Examples:
      pkm add note "Biology lecture notes"
      pkm add note "DNA info" --topics "Biology" --course "BIO101"
      pkm add task "Study for exam" --priority high
    """
    pass


@add.command(name="note")
@click.argument("content", required=True)
@click.option("--course", "-c", help="Assign to course (leaves inbox if omitted)")
@click.option("--topics", "-t", multiple=True, help="Add topic tags (can use multiple times)")
@click.pass_context
def add_note(ctx: click.Context, content: str, course: str | None, topics: tuple[str, ...]) -> None:
    """Add a new note to your inbox or directly to a course.

    \b
    CONTENT: Note content (use quotes for multi-word or multi-line notes)

    \b
    Options:
      -c, --course TEXT    Assign to a course (e.g., "Biology 101")
      -t, --topics TEXT    Add topic tags (use multiple times for multiple topics)

    \b
    Examples:
      # Quick inbox capture
      pkm add note "Photosynthesis converts light to chemical energy"

      # Note with course
      pkm add note "Lecture summary" --course "Biology 101"

      # Note with multiple topics
      pkm add note "Cell division process" \\
        --topics "Biology" \\
        --topics "Cell Structure" \\
        --topics "Mitosis"

      # Multi-line note
      pkm add note "Key points:
      - Light reactions in thylakoid
      - Calvin cycle in stroma
      - Produces glucose"

    Notes without a course are stored in your inbox for later organization.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = NoteService(data_dir)

        note = service.create_note(
            content=content,
            course=course,
            topics=list(topics) if topics else None,
        )

        location = f"course '{course}'" if course else "inbox"
        success(f"Note created: {note.id} in {location}")

        if topics:
            success(f"Tagged with: {', '.join(topics)}")

    except Exception as e:
        error(f"Failed to create note: {e}")
        ctx.exit(1)


@add.command(name="task")
@click.argument("title", required=True)
@click.option("--due", "-d", help="Due date (e.g., 'tomorrow', 'next Friday', '2025-12-01', 'Friday 11:59pm')")
@click.option("--priority", "-p", type=click.Choice(["high", "medium", "low"]), default="medium", help="Task priority: high, medium (default), or low")
@click.option("--course", "-c", help="Assign to course (leaves inbox if omitted)")
@click.pass_context
def add_task(ctx: click.Context, title: str, due: str | None, priority: str, course: str | None) -> None:
    """Add a new task to your inbox or directly to a course.

    \b
    TITLE: Task description or title

    \b
    Options:
      -d, --due TEXT         Due date (natural language or YYYY-MM-DD)
      -p, --priority TEXT    Priority level: high, medium, low (default: medium)
      -c, --course TEXT      Assign to a course (e.g., "Math 201")

    \b
    Examples:
      # Quick task
      pkm add task "Submit lab report"

      # Task with due date
      pkm add task "Submit lab report" --due "Friday 11:59pm"
      pkm add task "Study for exam" --due "tomorrow"
      pkm add task "Final project" --due "2025-12-15"

      # High-priority task
      pkm add task "Study for midterm" --priority high

      # Task with course
      pkm add task "Complete problem set 5" --course "Math 201"

      # Combine options
      pkm add task "Finish research paper" \\
        --due "next Friday" \\
        --priority high \\
        --course "English 101"

    \b
    Priority Levels:
      high   - Urgent, important deadlines
      medium - Normal tasks (default)
      low    - Nice to have, flexible timing

    \b
    Due Date Formats:
      Natural: "tomorrow", "next Friday", "in 3 days"
      ISO:     "2025-12-01"
      Human:   "Dec 1", "Friday 11:59pm"

    Tasks without a course are stored in your inbox for later organization.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = TaskService(data_dir)

        # Parse due date
        due_date = None
        if due:
            due_date = parse_due_date(due)
            if due_date is None:
                error(f"Could not parse due date: '{due}'")
                info("Try formats like: 'tomorrow', 'next Friday', '2025-12-01', 'Friday 11:59pm'")
                ctx.exit(1)

        task = service.create_task(
            title=title,
            due_date=due_date,
            priority=priority,
            course=course,
        )

        location = f"course '{course}'" if course else "inbox"
        success(f"Task created: {task.id} in {location}")

        if due_date:
            success(f"Due: {format_due_date(due_date)}")

        if priority != "medium":
            success(f"Priority: {priority}")

    except Exception as e:
        error(f"Failed to create task: {e}")
        ctx.exit(1)
