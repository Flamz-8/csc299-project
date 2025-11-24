"""Task management commands."""


import click

from pkm.cli.add import get_data_dir
from pkm.cli.helpers import error, info, success
from pkm.cli.main import cli
from pkm.services.task_service import TaskService


@cli.group()
def task() -> None:
    """Manage tasks (complete, add subtasks).

    \b
    Commands:
      pkm task complete TASK_ID       - Mark task as done
      pkm task add-subtask TASK_ID    - Add a subtask/bullet point
      pkm task check-subtask TASK_ID  - Mark subtask as complete

    \b
    Examples:
      pkm task complete t_20251123_140000_xyz
      pkm task add-subtask t_20251123_140000_xyz "Review chapter 1"
      pkm task check-subtask t_20251123_140000_xyz t_20251123_140000_xyz_sub_1
    """
    pass


@task.command(name="complete")
@click.argument("task_id", required=True)
@click.pass_context
def complete_task(ctx: click.Context, task_id: str) -> None:
    """Mark a task as completed.

    \b
    TASK_ID: The ID of the task to complete

    \b
    Examples:
      # Complete a task
      pkm task complete t_20251123_140000_xyz

      # With custom data directory
      pkm --data-dir ~/study task complete t_20251123_140000_xyz

    Completed tasks are marked with a timestamp and won't appear in active task views.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = TaskService(data_dir)

        task = service.complete_task(task_id)

        if task is None:
            error(f"Task not found: {task_id}")
            ctx.exit(1)

        success(f"✓ Task completed: {task.title}")
        if task.completed_at:
            info(f"Completed at: {task.completed_at.strftime('%Y-%m-%d %H:%M')}")

    except Exception as e:
        error(f"Failed to complete task: {e}")
        ctx.exit(1)


@task.command(name="add-subtask")
@click.argument("task_id", required=True)
@click.argument("title", required=True)
@click.pass_context
def add_subtask(ctx: click.Context, task_id: str, title: str) -> None:
    """Add a subtask (bullet point) to a task.

    \b
    TASK_ID: The parent task ID
    TITLE:   The subtask description

    \b
    Examples:
      # Add a subtask
      pkm task add-subtask t_20251123_140000_xyz "Review chapter 1"

      # Add multiple subtasks
      pkm task add-subtask t_20251123_140000_xyz "Read sections 1-3"
      pkm task add-subtask t_20251123_140000_xyz "Complete practice problems"
      pkm task add-subtask t_20251123_140000_xyz "Write summary"

    Subtasks help break down larger tasks into manageable steps.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = TaskService(data_dir)

        task = service.add_subtask(task_id, title)

        if task is None:
            error(f"Task not found: {task_id}")
            ctx.exit(1)

        success(f"Subtask added to '{task.title}'")
        info(f"Total subtasks: {len(task.subtasks)}")

        # Show progress
        completed = sum(1 for sub in task.subtasks if sub.completed)
        info(f"Progress: {completed}/{len(task.subtasks)} completed")

    except Exception as e:
        error(f"Failed to add subtask: {e}")
        ctx.exit(1)


@task.command(name="check-subtask")
@click.argument("task_id", required=True)
@click.argument("subtask_id", required=True, type=int)
@click.pass_context
def check_subtask(ctx: click.Context, task_id: str, subtask_id: int) -> None:
    """Mark a subtask as completed.

    \b
    TASK_ID:    The parent task ID
    SUBTASK_ID: The subtask number (integer, e.g., 1, 2, 3)

    \b
    Examples:
      # Complete subtask #1
      pkm task check-subtask t_20251123_140000_xyz 1

      # Complete subtask #2
      pkm task check-subtask t_20251123_140000_xyz 2

      # View task with subtasks first
      pkm view inbox

    Completed subtasks are marked with ✓ in task views.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = TaskService(data_dir)

        task = service.complete_subtask(task_id, subtask_id)

        if task is None:
            error(f"Task or subtask not found: {task_id} / subtask #{subtask_id}")
            ctx.exit(1)

        # Find the subtask to show title
        subtask_title = None
        for sub in task.subtasks:
            if sub.id == subtask_id:
                subtask_title = sub.title
                break

        success(f"✓ Subtask completed: {subtask_title}")

        # Show progress
        completed = sum(1 for sub in task.subtasks if sub.completed)
        info(f"Progress: {completed}/{len(task.subtasks)} completed")

    except Exception as e:
        error(f"Failed to complete subtask: {e}")
        ctx.exit(1)


@task.command(name="link-note")
@click.argument("task_id", required=True)
@click.argument("note_id", required=True)
@click.pass_context
def link_note(ctx: click.Context, task_id: str, note_id: str) -> None:
    """Link a note to a task for reference.

    \b
    TASK_ID: The task ID to link to
    NOTE_ID: The note ID to link

    \b
    Examples:
      pkm task link-note t_20251123_140000_xyz n_20251123_140000_abc

    \b
    Why Link Notes to Tasks?
      - Attach reference materials to tasks
      - Connect lecture notes to related assignments
      - Keep all context for a task in one place

    \b
    View linked notes:
      pkm view task TASK_ID
    """
    try:
        data_dir = get_data_dir(ctx)
        task_service = TaskService(data_dir)

        # Import note service to verify note exists
        from pkm.services.note_service import NoteService
        note_service = NoteService(data_dir)

        # Verify note exists
        note = note_service.get_note(note_id)
        if note is None:
            error(f"Note not found: {note_id}")
            info("Use 'pkm view inbox' or 'pkm view course' to see note IDs")
            ctx.exit(1)

        # Link the note to the task
        task = task_service.link_note(task_id, note_id)

        if task is None:
            error(f"Task not found: {task_id}")
            info("Use 'pkm view inbox' or 'pkm view course' to see task IDs")
            ctx.exit(1)

        success(f"Note linked to task: {task.title}")
        info(f"Note: {note.content[:50]}..." if len(note.content) > 50 else f"Note: {note.content}")

    except Exception as e:
        error(f"Failed to link note: {e}")
        ctx.exit(1)


@task.command(name="unlink-note")
@click.argument("task_id", required=True)
@click.argument("note_id", required=True)
@click.pass_context
def unlink_note(ctx: click.Context, task_id: str, note_id: str) -> None:
    """Unlink a note from a task.

    \b
    TASK_ID: The task ID to unlink from
    NOTE_ID: The note ID to unlink

    \b
    Examples:
      pkm task unlink-note t_20251123_140000_xyz n_20251123_140000_abc
    """
    try:
        data_dir = get_data_dir(ctx)
        service = TaskService(data_dir)

        task = service.unlink_note(task_id, note_id)

        if task is None:
            error(f"Task not found: {task_id}")
            ctx.exit(1)

        success(f"Note unlinked from task: {task.title}")

    except Exception as e:
        error(f"Failed to unlink note: {e}")
        ctx.exit(1)
