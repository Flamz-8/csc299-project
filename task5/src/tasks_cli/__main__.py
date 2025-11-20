"""Main entry point for the tasks CLI."""

import argparse
import sys


def main() -> int:
    """Main entry point for tasks CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        prog="tasks",
        description="Command-line task management",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add subcommand
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # List subcommand
    subparsers.add_parser("list", help="List all tasks")

    args = parser.parse_args()

    try:
        if args.command == "add":
            from tasks_cli.commands.add import add_command

            return add_command(args.description)
        if args.command == "list":
            from tasks_cli.commands.list import list_command

            return list_command()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
