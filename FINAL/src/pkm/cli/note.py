"""Note management commands."""

from pathlib import Path

import click

from pkm.cli.helpers import error, info, success, warning
from pkm.cli.main import cli
from pkm.services.note_service import NoteService
from pkm.services.task_service import TaskService
from pkm.utils.editor import open_in_editor


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
def note() -> None:
    """Manage notes - edit, delete, and organize.

    \b
    Commands:
      pkm note edit NOTE_ID       - Edit note in external editor
      pkm note delete NOTE_ID     - Delete a note
      pkm note add-topic NOTE_ID  - Add topics to a note
      pkm note remove-topic       - Remove topic from a note

    \b
    Examples:
      pkm note edit n_20251123_142055_abc
      pkm note delete n_20251123_142055_abc
      pkm note add-topic n_20251123_142055_abc "Biology"
    """
    pass


@note.command(name="edit")
@click.argument("note_id", required=True)
@click.pass_context
def edit_note(ctx: click.Context, note_id: str) -> None:
    """Edit a note in your external editor.

    \b
    NOTE_ID: The note ID to edit (use 'pkm view inbox' to see IDs)

    \b
    Examples:
      pkm note edit n_20251123_142055_abc

    \b
    Editor Selection:
      1. Uses $EDITOR environment variable if set
      2. Falls back to platform default:
         - Windows: notepad.exe
         - macOS/Linux: nano

    \b
    To set your preferred editor:
      # Linux/macOS
      export EDITOR=vim

      # Windows PowerShell
      $env:EDITOR = "code --wait"

    The editor will open with the current note content. Save and close
    to update the note. If you exit without changes, the note is unchanged.
    """
    try:
        data_dir = get_data_dir(ctx)
        service = NoteService(data_dir)

        # Get the note
        note = service.get_note(note_id)
        if not note:
            error(f"Note not found: {note_id}")
            info("Use 'pkm view inbox' or 'pkm view course' to see note IDs")
            ctx.exit(1)

        info(f"Opening note {note_id} in editor...")

        # Open in editor
        try:
            edited_content = open_in_editor(note.content)
        except RuntimeError as e:
            error(str(e))
            ctx.exit(1)

        # Check if content was actually edited
        if edited_content is None:
            warning("No changes made to note")
            ctx.exit(0)

        # Update the note
        updated_note = service.update_note(note_id, edited_content)
        if updated_note:
            success(f"Note updated: {note_id}")
        else:
            error(f"Failed to update note: {note_id}")
            ctx.exit(1)

    except Exception as e:
        error(f"Failed to edit note: {e}")
        ctx.exit(1)


@note.command(name="delete")
@click.argument("note_id", required=True)
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def delete_note(ctx: click.Context, note_id: str, yes: bool) -> None:
    """Delete a note.

    \b
    NOTE_ID: The note ID to delete (use 'pkm view inbox' to see IDs)

    \b
    Options:
      -y, --yes    Skip confirmation prompt

    \b
    Examples:
      # With confirmation
      pkm note delete n_20251123_142055_abc

      # Skip confirmation
      pkm note delete n_20251123_142055_abc -y

    WARNING: This action cannot be undone!
    """
    try:
        data_dir = get_data_dir(ctx)
        note_service = NoteService(data_dir)
        task_service = TaskService(data_dir)

        # Get the note
        note = note_service.get_note(note_id)
        if not note:
            error(f"Note not found: {note_id}")
            info("Use 'pkm view inbox' or 'pkm view course' to see note IDs")
            ctx.exit(1)

        # Check if note is linked to any tasks
        if note.linked_from_tasks:
            warning(f"Note is linked to {len(note.linked_from_tasks)} task(s)")
            info("Linked tasks:")
            for task_id in note.linked_from_tasks:
                task = task_service.get_task(task_id)
                if task:
                    info(f"  - {task.title} ({task_id})")

        # Confirm deletion
        if not yes:
            preview = note.content[:50] + "..." if len(note.content) > 50 else note.content
            click.echo(f"\nNote: {preview}")
            if not click.confirm("\nAre you sure you want to delete this note?"):
                warning("Deletion cancelled")
                ctx.exit(0)

        # Delete the note
        if note_service.delete_note(note_id):
            success(f"Note deleted: {note_id}")
        else:
            error(f"Failed to delete note: {note_id}")
            ctx.exit(1)

    except Exception as e:
        error(f"Failed to delete note: {e}")
        ctx.exit(1)


@note.command(name="add-topic")
@click.argument("note_id", required=True)
@click.argument("topics", nargs=-1, required=True)
@click.pass_context
def add_topic_to_note(ctx: click.Context, note_id: str, topics: tuple[str, ...]) -> None:
    """Add topics to a note.

    \b
    NOTE_ID: The note ID to add topics to
    TOPICS: One or more topics to add

    \b
    Examples:
      pkm note add-topic n_20251123_142055_abc "Biology"
      pkm note add-topic n_20251123_142055_abc "Biology" "Cell Structure"
    """
    try:
        data_dir = get_data_dir(ctx)
        service = NoteService(data_dir)

        # Add topics
        note = service.add_topics(note_id, list(topics))
        if note:
            success(f"Topics added to {note_id}")
            success(f"Current topics: {', '.join(note.topics)}")
        else:
            error(f"Note not found: {note_id}")
            ctx.exit(1)

    except Exception as e:
        error(f"Failed to add topics: {e}")
        ctx.exit(1)


@note.command(name="remove-topic")
@click.argument("note_id", required=True)
@click.argument("topic", required=True)
@click.pass_context
def remove_topic_from_note(ctx: click.Context, note_id: str, topic: str) -> None:
    """Remove a topic from a note.

    \b
    NOTE_ID: The note ID to remove topic from
    TOPIC: The topic to remove

    \b
    Examples:
      pkm note remove-topic n_20251123_142055_abc "Biology"
    """
    try:
        data_dir = get_data_dir(ctx)
        service = NoteService(data_dir)

        # Remove topic
        note = service.remove_topic(note_id, topic)
        if note:
            if topic in note.topics:
                warning(f"Topic '{topic}' not found in note")
            else:
                success(f"Topic '{topic}' removed from {note_id}")
            if note.topics:
                success(f"Remaining topics: {', '.join(note.topics)}")
            else:
                info("Note has no topics")
        else:
            error(f"Note not found: {note_id}")
            ctx.exit(1)

    except Exception as e:
        error(f"Failed to remove topic: {e}")
        ctx.exit(1)
