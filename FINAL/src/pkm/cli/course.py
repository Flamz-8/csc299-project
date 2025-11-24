"""Course management commands."""

import click

from pkm.cli.add import get_data_dir
from pkm.cli.helpers import error, info, success, warning
from pkm.cli.main import cli
from pkm.services.course_service import CourseService


@cli.group()
def course() -> None:
    """Manage courses - delete and reorganize.

    \b
    Commands:
      pkm course delete COURSE_NAME    - Delete a course

    \b
    Examples:
      pkm course delete "Biology 101"
      pkm course delete "Math 201" --delete-items
    """
    pass


@course.command(name="delete")
@click.argument("course_name", required=True)
@click.option("--delete-items", is_flag=True, help="Delete all notes/tasks instead of moving to inbox")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def delete_course(ctx: click.Context, course_name: str, delete_items: bool, yes: bool) -> None:
    """Delete a course and handle its items.

    \b
    COURSE_NAME: The name of the course to delete

    \b
    Options:
      --delete-items    Delete all notes and tasks (default: move to inbox)
      -y, --yes         Skip confirmation prompt

    \b
    Examples:
      # Delete course and move items to inbox
      pkm course delete "Biology 101"

      # Delete course and all its items
      pkm course delete "Old Course" --delete-items

      # Skip confirmation
      pkm course delete "Test Course" -y

    By default, notes and tasks are moved to inbox. Use --delete-items to
    permanently delete them (WARNING: cannot be undone!)
    """
    try:
        data_dir = get_data_dir(ctx)
        service = CourseService(data_dir)

        # Check if course exists
        course = service.get_course(course_name)
        if not course:
            error(f"Course not found: {course_name}")
            info("Use 'pkm view courses' to see available courses")
            ctx.exit(1)

        # Show what will happen
        if not yes:
            click.echo(f"\nCourse: {course_name}")
            click.echo(f"Notes: {course.note_count}")
            click.echo(f"Tasks: {course.task_count}")
            
            if delete_items:
                warning("⚠️  All notes and tasks will be PERMANENTLY DELETED!")
                click.echo("This action cannot be undone.")
            else:
                click.echo("Notes and tasks will be moved to inbox.")
            
            if not click.confirm(f"\nAre you sure you want to delete '{course_name}'?"):
                warning("Deletion cancelled")
                ctx.exit(0)

        # Delete the course
        counts = service.delete_course(course_name, reassign_to_inbox=not delete_items)

        if delete_items:
            success(f"Course '{course_name}' deleted")
            warning(f"Deleted {counts['notes']} notes and {counts['tasks']} tasks")
        else:
            success(f"Course '{course_name}' deleted")
            info(f"Moved {counts['notes']} notes and {counts['tasks']} tasks to inbox")

    except Exception as e:
        error(f"Failed to delete course: {e}")
        ctx.exit(1)
