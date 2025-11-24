"""Search commands for finding notes and tasks."""


import click
from rich.console import Console

from pkm.cli.add import get_data_dir
from pkm.cli.helpers import create_table, error, info, truncate
from pkm.cli.main import cli
from pkm.services.search_service import SearchService
from pkm.utils.date_parser import format_due_date


@cli.command()
@click.argument("query", required=True)
@click.option("--type", "-t", type=click.Choice(["notes", "tasks"]), help="Filter by type")
@click.option("--course", "-c", help="Filter by course name")
@click.option("--topic", help="Filter by topic (notes only)")
@click.pass_context
def search(ctx: click.Context, query: str, type: str | None, course: str | None, topic: str | None) -> None:
    """Search for notes and tasks by keyword.

    \b
    QUERY: Search term (searches content, titles, topics, courses)

    \b
    Options:
      -t, --type TEXT     Filter: notes or tasks
      -c, --course TEXT   Filter by course name
      --topic TEXT        Filter by topic (notes only)

    \b
    Examples:
      # Search everything
      pkm search "photosynthesis"

      # Search only notes
      pkm search "exam" --type notes

      # Search in a specific course
      pkm search "chapter" --course "Biology 101"

      # Search by topic
      pkm search "cell" --topic "Biology"

    Search is case-insensitive and matches partial words.
    """
    try:
        data_dir = get_data_dir(ctx)
        search_service = SearchService(data_dir)

        notes, tasks = search_service.search(query, type, course, topic)

        if not notes and not tasks:
            info(f"No results found for '{query}'")
            if course or topic:
                info("Try removing filters or using a different search term.")
            return

        Console().print(f"\n[bold]🔍 Search Results for '{query}'[/bold]")
        Console().print()

        # Display notes
        if notes:
            table = create_table(f"Notes ({len(notes)})", ["Content", "Course", "Topics"])
            for note in notes[:20]:  # Show first 20
                # Highlight query in content
                content_display = truncate(note.content, 60)

                table.add_row(
                    content_display,
                    note.course or "-",
                    ", ".join(note.topics[:3]) if note.topics else "-",
                )
            Console().print(table)
            if len(notes) > 20:
                info(f"Showing 20 of {len(notes)} notes")
            Console().print()

        # Display tasks
        if tasks:
            table = create_table(f"Tasks ({len(tasks)})", ["Title", "Due", "Course", "Status"])
            for task in tasks[:20]:  # Show first 20
                due_display = format_due_date(task.due_date) if task.due_date else "-"
                status = "✓ Done" if task.completed else "Active"

                table.add_row(
                    truncate(task.title, 40),
                    truncate(due_display, 20),
                    task.course or "-",
                    status,
                )
            Console().print(table)
            if len(tasks) > 20:
                info(f"Showing 20 of {len(tasks)} tasks")
            Console().print()

        total = len(notes) + len(tasks)
        info(f"Total: {total} results ({len(notes)} notes, {len(tasks)} tasks)")

    except Exception as e:
        error(f"Search failed: {e}")
        ctx.exit(1)
