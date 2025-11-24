"""Pytest configuration and shared fixtures."""

import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_data_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def empty_data_file(temp_data_dir: Path) -> Path:
    """Create an empty data.json file."""
    data_file = temp_data_dir / "data.json"
    data_file.write_text(json.dumps({"notes": [], "tasks": [], "courses": []}))
    return data_file


@pytest.fixture
def sample_data_file(temp_data_dir: Path) -> Path:
    """Create a data.json file with sample data."""
    data_file = temp_data_dir / "data.json"
    sample_data = {
        "notes": [
            {
                "id": "n1",
                "content": "Test note 1",
                "created_at": "2025-11-23T10:00:00",
                "modified_at": "2025-11-23T10:00:00",
                "course": None,
                "topics": [],
                "linked_from_tasks": [],
            }
        ],
        "tasks": [
            {
                "id": "t1",
                "title": "Test task 1",
                "created_at": "2025-11-23T11:00:00",
                "due_date": None,
                "priority": "medium",
                "completed": False,
                "completed_at": None,
                "course": None,
                "linked_notes": [],
                "subtasks": [],
            }
        ],
        "courses": [],
    }
    data_file.write_text(json.dumps(sample_data))
    return data_file
