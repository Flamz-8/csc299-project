"""
Task3 - Personal Knowledge Management System

This package provides a unified PKMS that combines task and knowledge management
in a single system with bi-directional linking capabilities.

Testing:
    # Run all tests
    uv run pytest

    # Run specific test categories
    uv run pytest tests/test_search.py  # Search functionality
    uv run pytest tests/test_core.py    # Core functionality
    uv run pytest tests/test_linking.py # Task-Note linking

    # Run specific test
    uv run pytest tests/test_search.py::test_search_by_title
"""

def inc(n: int) -> int:
    return n + 1

def main() -> None:
    """Run example usage of the unified PKMS"""
    from task3.pkms import PKMS  # Updated import to use unified PKMS
    
    pkms = PKMS()
    
    # Create a task and related note
    task_id = pkms.add_task(
        title="Research PKMS",
        description="Study knowledge management systems",
        tags=["pkms", "research"]
    )
    
    note_id = pkms.add_note(
        title="PKMS Notes",
        content="Key concepts in knowledge management...",
        tags=["pkms", "notes"]
    )
    
    # Link task and note
    pkms.link_task_note(task_id, note_id)
    
    # Search across both tasks and notes
    tasks, notes = pkms.search("pkms")
    print("Found Tasks:", [t.title for t in tasks])
    print("Found Notes:", [n.title for n in notes])

if __name__ == "__main__":
    main()
