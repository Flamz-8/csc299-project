"""Organization commands for assigning items to courses."""


import click

from pkm.cli.add import get_data_dir
from pkm.cli.helpers import error, info, success
from pkm.cli.main import cli
from pkm.services.note_service import NoteService
from pkm.services.task_service import TaskService


@cli.group()
def organize() -> None:
    """Organize notes and tasks by assigning to courses.

    \b
    Commands:
      pkm organize note NOTE_ID --course NAME    - Move note to course
      pkm organize task TASK_ID --course NAME    - Move task to course

    \b
    Examples:
      pkm organize note n_20251123_140000_xyz --course "Biology 101"
      pkm organize task t_20251123_140000_abc --course "Math 201"

    Use this to move items from your inbox into organized courses.
    """
    pass


@organize.command(name="note")
@click.argument("note_id", required=True)
@click.option("--course", "-c", required=True, help="Course name to assign")
@click.option("--add-topics", "-t", multiple=True, help="Add additional topics")
@click.pass_context
def organize_note(ctx: click.Context, note_id: str, course: str, add_topics: tuple[str, ...]) -> None:
    """Assign a note to a course (move from inbox).

    \b
    NOTE_ID: The ID of the note to organize

    \b
    Options:
      -c, --course TEXT       Course name (required)
      -t, --add-topics TEXT   Add topics (can use multiple times)

    \b
    Examples:
      # Move note to course
      pkm organize note n_20251123_140000_xyz --course "Biology 101"

      # Move and add topics
      pkm organize note n_20251123_140000_xyz \\
        --course "Biology 101" \\
        --add-topics "Photosynthesis" \\
        --add-topics "Cell Structure"

    Organized notes no longer appear in your inbox.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = NoteService(data_dir)

        # Organize to course
        note = service.organize_note(note_id, course)

        if note is None:
            error(f"Note not found: {note_id}")
            ctx.exit(1)

        # Add topics if specified
        if add_topics:
            note = service.add_topics(note_id, list(add_topics))

        success(f"Note organized to '{course}'")

        if add_topics:
            info(f"Topics added: {', '.join(add_topics)}")

    except Exception as e:
        error(f"Failed to organize note: {e}")
        ctx.exit(1)


@organize.command(name="task")
@click.argument("task_id", required=True)
@click.option("--course", "-c", required=True, help="Course name to assign")
@click.pass_context
def organize_task(ctx: click.Context, task_id: str, course: str) -> None:
    """Assign a task to a course (move from inbox).

    \b
    TASK_ID: The ID of the task to organize

    \b
    Options:
      -c, --course TEXT    Course name (required)

    \b
    Examples:
      # Move task to course
      pkm organize task t_20251123_140000_xyz --course "Math 201"

      # Organize multiple tasks
      pkm organize task t_123 --course "Biology 101"
      pkm organize task t_456 --course "Biology 101"

    Organized tasks no longer appear in your inbox.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = TaskService(data_dir)

        task = service.organize_task(task_id, course)

        if task is None:
            error(f"Task not found: {task_id}")
            ctx.exit(1)

        success(f"Task organized to '{course}'")
        info(f"Title: {task.title}")

    except Exception as e:
        error(f"Failed to organize task: {e}")
        ctx.exit(1)
