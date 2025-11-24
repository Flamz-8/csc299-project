"""Unit tests for storage layer."""

import json
from pathlib import Path

import pytest

from pkm.storage.json_store import JSONStore
from pkm.storage.schema import create_empty_schema


class TestJSONStore:
    """Tests for JSONStore."""

    def test_load_nonexistent_file(self, temp_data_dir: Path) -> None:
        """Test loading when file doesn't exist returns empty schema."""
        store = JSONStore(temp_data_dir / "data.json")
        data = store.load()
        assert data["notes"] == []
        assert data["tasks"] == []
        assert data["courses"] == []

    def test_save_and_load(self, temp_data_dir: Path) -> None:
        """Test saving and loading data."""
        store = JSONStore(temp_data_dir / "data.json")
        data = create_empty_schema()
        data["notes"].append(
            {
                "id": "n1",
                "content": "Test note",
                "created_at": "2025-11-23T10:00:00",
                "modified_at": "2025-11-23T10:00:00",
                "course": None,
                "topics": [],
                "linked_from_tasks": [],
            }
        )

        store.save(data)
        loaded = store.load()

        assert len(loaded["notes"]) == 1
        assert loaded["notes"][0]["id"] == "n1"

    def test_atomic_write_creates_temp_file(self, temp_data_dir: Path) -> None:
        """Test that save uses atomic write with temp file."""
        store = JSONStore(temp_data_dir / "data.json")
        data = create_empty_schema()

        store.save(data)

        # Temp file should not exist after save
        assert not store.tmp_file.exists()
        # Final file should exist
        assert store.data_file.exists()

    def test_backup_creation(self, temp_data_dir: Path) -> None:
        """Test that backup is created when overwriting existing file."""
        store = JSONStore(temp_data_dir / "data.json")

        # Save initial data
        data1 = create_empty_schema()
        data1["notes"].append({"id": "note1", "content": "First version"})
        store.save(data1)

        # Save updated data
        data2 = create_empty_schema()
        data2["notes"].append({"id": "note2", "content": "Second version"})
        store.save(data2)

        # Backup should exist
        assert store.backup_exists()

        # Backup should contain first version
        with open(store.bak_file, "r") as f:
            backup = json.load(f)
            assert backup["notes"][0]["id"] == "note1"

    def test_corrupted_file_recovery(self, temp_data_dir: Path) -> None:
        """Test recovery from corrupted data file using backup."""
        store = JSONStore(temp_data_dir / "data.json")

        # Create valid backup
        valid_data = create_empty_schema()
        store.bak_file.write_text(json.dumps(valid_data))

        # Create corrupted main file
        store.data_file.write_text("INVALID JSON{{{")

        # Load should recover from backup
        loaded = store.load()
        assert loaded["notes"] == []
        assert loaded["tasks"] == []

    def test_restore_from_backup(self, temp_data_dir: Path) -> None:
        """Test manual restoration from backup."""
        store = JSONStore(temp_data_dir / "data.json")

        # Create backup
        backup_data = create_empty_schema()
        backup_data["notes"].append({"id": "backup_note"})
        store.bak_file.write_text(json.dumps(backup_data))

        # Create different main file
        main_data = create_empty_schema()
        store.data_file.write_text(json.dumps(main_data))

        # Restore from backup
        store.restore_from_backup()

        # Main file should now have backup content
        loaded = store.load()
        assert len(loaded["notes"]) == 1
        assert loaded["notes"][0]["id"] == "backup_note"

    def test_restore_without_backup_fails(self, temp_data_dir: Path) -> None:
        """Test that restore fails when no backup exists."""
        store = JSONStore(temp_data_dir / "data.json")

        with pytest.raises(FileNotFoundError):
            store.restore_from_backup()
