"""Edge case tests for corrupted data handling."""

import json
from pathlib import Path

import pytest

from pkm.storage.json_store import JSONStore
from pkm.storage.schema import create_empty_schema


class TestCorruptedData:
    """Tests for handling corrupted data files."""

    def test_invalid_json_with_backup(self, temp_data_dir: Path) -> None:
        """Test that corrupted JSON recovers from backup."""
        store = JSONStore(temp_data_dir / "data.json")

        # Create valid backup
        valid_data = create_empty_schema()
        valid_data["notes"].append(
            {
                "id": "n1",
                "content": "Backup note",
                "created_at": "2025-11-23T10:00:00",
                "modified_at": "2025-11-23T10:00:00",
                "course": None,
                "topics": [],
                "linked_from_tasks": [],
            }
        )
        store.bak_file.write_text(json.dumps(valid_data))

        # Corrupt main file
        store.data_file.write_text("INVALID{JSON}DATA")

        # Should recover from backup
        loaded = store.load()
        assert len(loaded["notes"]) == 1
        assert loaded["notes"][0]["content"] == "Backup note"

    def test_invalid_json_without_backup(self, temp_data_dir: Path) -> None:
        """Test that corrupted JSON without backup raises error."""
        store = JSONStore(temp_data_dir / "data.json")

        # Corrupt main file with no backup
        store.data_file.write_text("INVALID JSON")

        with pytest.raises(ValueError, match="Corrupted data file"):
            store.load()

    def test_incomplete_schema_auto_fills(self, temp_data_dir: Path) -> None:
        """Test that incomplete schema is auto-filled with missing keys."""
        store = JSONStore(temp_data_dir / "data.json")

        # Create file with missing keys
        incomplete_data = {"notes": []}  # Missing tasks and courses
        store.data_file.write_text(json.dumps(incomplete_data))

        loaded = store.load()
        assert "notes" in loaded
        assert "tasks" in loaded
        assert "courses" in loaded
        assert loaded["tasks"] == []
        assert loaded["courses"] == []

    def test_empty_file(self, temp_data_dir: Path) -> None:
        """Test handling of empty data file."""
        store = JSONStore(temp_data_dir / "data.json")
        store.data_file.write_text("")

        with pytest.raises(ValueError, match="Corrupted data file"):
            store.load()

    def test_partial_json(self, temp_data_dir: Path) -> None:
        """Test handling of truncated JSON."""
        store = JSONStore(temp_data_dir / "data.json")
        store.data_file.write_text('{"notes": [{"id": "n_202')

        with pytest.raises(ValueError, match="Corrupted data file"):
            store.load()
