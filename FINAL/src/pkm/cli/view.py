"""View commands for displaying notes and tasks."""

from datetime import datetime

import click
from rich.console import Console

from pkm.cli.add import get_data_dir
from pkm.cli.helpers import create_table, format_datetime, info, truncate
from pkm.cli.main import cli
from pkm.services.course_service import CourseService
from pkm.services.note_service import NoteService
from pkm.services.task_service import TaskService
from pkm.utils.date_parser import format_due_date


@cli.group()
def view() -> None:
    """View notes and tasks in various formats.

    \b
    Available views:
      pkm view inbox    - Show unorganized notes and tasks
      pkm view today    - Tasks due today
      pkm view week     - Tasks due this week
      pkm view overdue  - Overdue tasks

    \b
    Coming soon:
      pkm view course   - Items by course (Phase 5)

    \b
    Examples:
      pkm view inbox
      pkm view today
      pkm view week
      pkm view inbox --data-dir ~/my-notes
    """
    pass


@view.command(name="inbox")
@click.pass_context
def view_inbox(ctx: click.Context) -> None:
    """View all unorganized notes and tasks in your inbox.

    \b
    Shows:
      - Notes without a course assignment
      - Tasks without a course assignment
      - Displayed in rich formatted tables
      - Sorted by creation date

    \b
    Examples:
      # View inbox
      pkm view inbox

      # View inbox with custom data location
      pkm --data-dir ~/study-notes view inbox

    \b
    The inbox is your temporary holding area for quick capture.
    Organize items later by assigning them to courses (coming in Phase 5).

    Empty inbox = all items organized!
    """
    data_dir = get_data_dir(ctx)
    note_service = NoteService(data_dir)
    task_service = TaskService(data_dir)

    inbox_notes = note_service.get_inbox_notes()
    inbox_tasks = task_service.get_inbox_tasks()

    if not inbox_notes and not inbox_tasks:
        info("Inbox is empty")
        return

    # Display notes
    if inbox_notes:
        table = create_table("Inbox Notes", ["Content", "Created", "Topics"])
        for note in inbox_notes:
            table.add_row(
                truncate(note.content, 60),
                format_datetime(note.created_at),
                ", ".join(note.topics) if note.topics else "-",
            )
        Console().print(table)
        Console().print()

    # Display tasks
    if inbox_tasks:
        table = create_table("Inbox Tasks", ["Title", "Due", "Priority", "Subtasks"])
        for task in inbox_tasks:
            priority_color = {
                "high": "[red]HIGH[/red]",
                "medium": "[yellow]MED[/yellow]",
                "low": "[green]LOW[/green]",
            }[task.priority]

            # Format due date
            due_display = format_due_date(task.due_date) if task.due_date else "-"

            # Format subtasks progress
            if task.subtasks:
                completed = sum(1 for sub in task.subtasks if sub.completed)
                subtasks_display = f"{completed}/{len(task.subtasks)} ✓"
            else:
                subtasks_display = "-"

            table.add_row(
                truncate(task.title, 40),
                truncate(due_display, 25),
                priority_color,
                subtasks_display,
            )
        Console().print(table)

    total = len(inbox_notes) + len(inbox_tasks)
    info(f"Total inbox items: {total} ({len(inbox_notes)} notes, {len(inbox_tasks)} tasks)")


@view.command(name="today")
@click.pass_context
def view_today(ctx: click.Context) -> None:
    """View tasks due today.

    \b
    Shows:
      - All tasks with due date = today
      - Excludes completed tasks
      - Sorted by priority (high → medium → low)

    \b
    Examples:
      # View today's tasks
      pkm view today

      # With custom data location
      pkm --data-dir ~/study-notes view today

    Use this command each morning to see what's on your plate for the day!
    """
    data_dir = get_data_dir(ctx)
    task_service = TaskService(data_dir)

    tasks = task_service.get_tasks_today()

    if not tasks:
        info("No tasks due today!")
        return

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: priority_order[t.priority])

    table = create_table(f"Tasks Due Today ({len(tasks)})", ["Title", "Due Time", "Priority", "Subtasks", "Course"])

    for task in tasks:
        priority_color = {
            "high": "[red]HIGH[/red]",
            "medium": "[yellow]MED[/yellow]",
            "low": "[green]LOW[/green]",
        }[task.priority]

        # Format due time (just time, not full date)
        due_time = task.due_date.strftime("%I:%M %p").replace(" 0", " ") if task.due_date else "-"

        # Format subtasks progress
        if task.subtasks:
            completed = sum(1 for sub in task.subtasks if sub.completed)
            subtasks_display = f"{completed}/{len(task.subtasks)} ✓"
        else:
            subtasks_display = "-"

        table.add_row(
            truncate(task.title, 35),
            due_time,
            priority_color,
            subtasks_display,
            task.course or "-",
        )

    Console().print(table)
    info(f"Total: {len(tasks)} tasks due today")


@view.command(name="week")
@click.pass_context
def view_week(ctx: click.Context) -> None:
    """View tasks due this week (next 7 days).

    \b
    Shows:
      - All tasks with due date within 7 days
      - Excludes completed tasks
      - Sorted by due date

    \b
    Examples:
      # View this week's tasks
      pkm view week

      # With custom data location
      pkm --data-dir ~/study-notes view week

    Great for weekly planning and seeing what's coming up!
    """
    data_dir = get_data_dir(ctx)
    task_service = TaskService(data_dir)

    tasks = task_service.get_tasks_this_week()

    if not tasks:
        info("No tasks due this week!")
        return

    # Sort by due date
    tasks.sort(key=lambda t: t.due_date if t.due_date else datetime.max)

    table = create_table(f"Tasks Due This Week ({len(tasks)})", ["Title", "Due", "Priority", "Subtasks", "Course"])

    for task in tasks:
        priority_color = {
            "high": "[red]HIGH[/red]",
            "medium": "[yellow]MED[/yellow]",
            "low": "[green]LOW[/green]",
        }[task.priority]

        # Format due date
        due_display = format_due_date(task.due_date) if task.due_date else "-"

        # Format subtasks progress
        if task.subtasks:
            completed = sum(1 for sub in task.subtasks if sub.completed)
            subtasks_display = f"{completed}/{len(task.subtasks)} ✓"
        else:
            subtasks_display = "-"

        table.add_row(
            truncate(task.title, 30),
            truncate(due_display, 25),
            priority_color,
            subtasks_display,
            task.course or "-",
        )

    Console().print(table)
    info(f"Total: {len(tasks)} tasks due within 7 days")


@view.command(name="overdue")
@click.pass_context
def view_overdue(ctx: click.Context) -> None:
    """View overdue tasks (past due date and not completed).

    \b
    Shows:
      - All tasks with due date < today
      - Only incomplete tasks
      - Sorted by how overdue (oldest first)
      - Highlighted in red

    \b
    Examples:
      # View overdue tasks
      pkm view overdue

      # With custom data location
      pkm --data-dir ~/study-notes view overdue

    Time to catch up on these! Complete or reschedule overdue tasks.
    """
    data_dir = get_data_dir(ctx)
    task_service = TaskService(data_dir)

    tasks = task_service.get_tasks_overdue()

    if not tasks:
        info("No overdue tasks - great job!")
        return

    # Sort by due date (oldest first)
    tasks.sort(key=lambda t: t.due_date if t.due_date else datetime.min)

    table = create_table(f"[red]Overdue Tasks ({len(tasks)})[/red]", ["Title", "Due", "Priority", "Subtasks", "Course"])

    for task in tasks:
        priority_color = {
            "high": "[red]HIGH[/red]",
            "medium": "[yellow]MED[/yellow]",
            "low": "[green]LOW[/green]",
        }[task.priority]

        # Format due date (highlight how overdue)
        due_display = f"[red]{format_due_date(task.due_date)}[/red]" if task.due_date else "-"

        # Format subtasks progress
        if task.subtasks:
            completed = sum(1 for sub in task.subtasks if sub.completed)
            subtasks_display = f"{completed}/{len(task.subtasks)} ✓"
        else:
            subtasks_display = "-"

        table.add_row(
            truncate(task.title, 30),
            truncate(due_display, 30),
            priority_color,
            subtasks_display,
            task.course or "-",
        )

    Console().print(table)
    info(f"[red]Total: {len(tasks)} overdue tasks[/red]")


@view.command(name="course")
@click.argument("course_name", required=True)
@click.pass_context
def view_course(ctx: click.Context, course_name: str) -> None:
    """View all notes and tasks for a specific course.

    \b
    COURSE_NAME: The course name (use quotes if it contains spaces)

    \b
    Shows:
      - All notes in the course
      - All tasks in the course
      - Grouped and formatted with rich tables

    \b
    Examples:
      # View a course
      pkm view course "Biology 101"

      # View course without spaces
      pkm view course Math201

    This helps you see all content related to a specific class.
    """
    data_dir = get_data_dir(ctx)
    note_service = NoteService(data_dir)
    task_service = TaskService(data_dir)

    notes = note_service.get_notes_by_course(course_name)
    tasks = task_service.get_tasks_by_course(course_name)

    if not notes and not tasks:
        info(f"No items found in course '{course_name}'")
        return

    Console().print(f"\n[bold]📚 {course_name}[/bold]")
    Console().print()

    # Display notes
    if notes:
        table = create_table(f"Notes ({len(notes)})", ["Content", "Created", "Topics"])
        for note in notes[:10]:  # Show first 10
            table.add_row(
                truncate(note.content, 50),
                format_datetime(note.created_at),
                ", ".join(note.topics) if note.topics else "-",
            )
        Console().print(table)
        if len(notes) > 10:
            info(f"Showing 10 of {len(notes)} notes")
        Console().print()

    # Display tasks
    if tasks:
        table = create_table(f"Tasks ({len(tasks)})", ["Title", "Due", "Priority", "Status"])
        for task in tasks:
            priority_color = {
                "high": "[red]HIGH[/red]",
                "medium": "[yellow]MED[/yellow]",
                "low": "[green]LOW[/green]",
            }[task.priority]

            due_display = format_due_date(task.due_date) if task.due_date else "-"
            status = "✓ Done" if task.completed else "Active"

            table.add_row(
                truncate(task.title, 40),
                truncate(due_display, 25),
                priority_color,
                status,
            )
        Console().print(table)
        Console().print()

    info(f"Total: {len(notes)} notes, {len(tasks)} tasks")


@view.command(name="courses")
@click.pass_context
def view_courses(ctx: click.Context) -> None:
    """List all courses with note and task counts.

    \b
    Shows:
      - All courses in your system
      - Number of notes per course
      - Number of tasks per course

    \b
    Examples:
      # List all courses
      pkm view courses

    Use this to see all your classes and their content at a glance.
    """
    data_dir = get_data_dir(ctx)
    course_service = CourseService(data_dir)

    courses = course_service.list_courses()

    if not courses:
        info("No courses found. Organize notes and tasks to create courses.")
        return

    table = create_table(f"Courses ({len(courses)})", ["Course", "Notes", "Tasks", "Total Items"])

    for course in courses:
        total = course.note_count + course.task_count
        table.add_row(
            course.name,
            str(course.note_count),
            str(course.task_count),
            str(total),
        )

    Console().print(table)

    total_notes = sum(c.note_count for c in courses)
    total_tasks = sum(c.task_count for c in courses)
    info(f"Total: {len(courses)} courses, {total_notes} notes, {total_tasks} tasks")


@view.command(name="task")
@click.argument("task_id", required=True)
@click.option("--expand", "-e", is_flag=True, help="Show full content of linked notes")
@click.pass_context
def view_task(ctx: click.Context, task_id: str, expand: bool) -> None:
    """View a task with all its details and linked notes.

    \b
    TASK_ID: The task ID to view

    \b
    Options:
      -e, --expand    Show full content of linked notes

    \b
    Examples:
      # View task details
      pkm view task t_20251123_140000_xyz

      # View with full note content
      pkm view task t_20251123_140000_xyz --expand

    \b
    Shows:
      - Task title and details
      - Due date and priority
      - Subtasks and progress
      - Linked notes (preview or full content)
    """
    from pkm.cli.helpers import error

    data_dir = get_data_dir(ctx)
    task_service = TaskService(data_dir)
    note_service = NoteService(data_dir)
    console = Console()

    # Get the task
    task = task_service.get_task(task_id)
    if not task:
        error(f"Task not found: {task_id}")
        info("Use 'pkm view inbox' or 'pkm view course' to see task IDs")
        ctx.exit(1)

    # Display task details
    console.print(f"\n[bold cyan]Task: {task.title}[/bold cyan]")
    console.print(f"ID: {task.id}")

    if task.course:
        console.print(f"Course: {task.course}")
    else:
        console.print("Course: [yellow](inbox)[/yellow]")

    if task.due_date:
        formatted_due = format_due_date(task.due_date)
        console.print(f"Due: {formatted_due}")

    console.print(f"Priority: {task.priority}")
    console.print(f"Status: {'[green]✓ Completed[/green]' if task.completed else '[yellow]Pending[/yellow]'}")

    # Show subtasks if any
    if task.subtasks:
        console.print(f"\n[bold]Subtasks ({len(task.subtasks)}):[/bold]")
        for subtask in task.subtasks:
            status = "✓" if subtask.completed else " "
            console.print(f"  [{status}] {subtask.id}. {subtask.title}")

        completed = sum(1 for s in task.subtasks if s.completed)
        console.print(f"\nProgress: {completed}/{len(task.subtasks)} completed")

    # Show linked notes
    if task.linked_notes:
        console.print(f"\n[bold]Linked Notes ({len(task.linked_notes)}):[/bold]")
        for note_id in task.linked_notes:
            note = note_service.get_note(note_id)
            if note:
                if expand:
                    console.print(f"\n[cyan]━━━ {note_id} ━━━[/cyan]")
                    console.print(note.content)
                    if note.topics:
                        console.print(f"Topics: {', '.join(note.topics)}")
                else:
                    preview = truncate(note.content, 60)
                    console.print(f"  • {note_id}: {preview}")

        if not expand:
            info("Use --expand to see full note content")
    else:
        console.print("\n[dim]No linked notes[/dim]")
        info("Use 'pkm task link-note TASK_ID NOTE_ID' to link notes")

    console.print()


@view.command(name="note")
@click.argument("note_id", required=True)
@click.pass_context
def view_note(ctx: click.Context, note_id: str) -> None:
    """View a note with all its details and referencing tasks.

    \b
    NOTE_ID: The note ID to view

    \b
    Examples:
      pkm view note n_20251123_140000_xyz

    \b
    Shows:
      - Note content
      - Topics
      - Course (if assigned)
      - Tasks that reference this note
    """
    from pkm.cli.helpers import error

    data_dir = get_data_dir(ctx)
    note_service = NoteService(data_dir)
    task_service = TaskService(data_dir)
    console = Console()

    # Get the note
    note = note_service.get_note(note_id)
    if not note:
        error(f"Note not found: {note_id}")
        info("Use 'pkm view inbox' or 'pkm view course' to see note IDs")
        ctx.exit(1)

    # Display note details
    console.print("\n[bold cyan]Note[/bold cyan]")
    console.print(f"ID: {note.id}")

    if note.course:
        console.print(f"Course: {note.course}")
    else:
        console.print("Course: [yellow](inbox)[/yellow]")

    if note.topics:
        console.print(f"Topics: {', '.join(note.topics)}")

    console.print(f"Created: {format_datetime(note.created_at)}")
    console.print(f"Modified: {format_datetime(note.modified_at)}")

    console.print("\n[bold]Content:[/bold]")
    console.print(note.content)

    # Show tasks that reference this note
    if note.linked_from_tasks:
        console.print(f"\n[bold]Referenced by Tasks ({len(note.linked_from_tasks)}):[/bold]")
        for task_id in note.linked_from_tasks:
            task = task_service.get_task(task_id)
            if task:
                status = "✓" if task.completed else " "
                priority_color = "red" if task.priority == "high" else "yellow" if task.priority == "medium" else "green"
                console.print(f"  [{status}] [{priority_color}]{task.priority:6}[/{priority_color}] {task.title} ({task_id})")
    else:
        console.print("\n[dim]No tasks reference this note[/dim]")
        info("Use 'pkm task link-note TASK_ID NOTE_ID' to link this note to a task")

    console.print()
