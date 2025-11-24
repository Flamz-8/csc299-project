"""JSON file storage with atomic writes."""

import json
import shutil
from pathlib import Path

from pkm.storage.schema import DataSchema, create_empty_schema


class JSONStore:
    """Handles JSON file I/O with atomic writes and backup creation.

    Ensures data integrity by:
    - Writing to temporary file first (.tmp)
    - Renaming to target file only if write succeeds
    - Creating backups before overwriting (.bak)
    """

    def __init__(self, data_file: Path) -> None:
        """Initialize JSON store.

        Args:
            data_file: Path to the data.json file
        """
        self.data_file = data_file
        self.tmp_file = data_file.with_suffix(".json.tmp")
        self.bak_file = data_file.with_suffix(".json.bak")

    def load(self) -> DataSchema:
        """Load data from JSON file.

        Returns:
            Data schema with notes, tasks, and courses

        Raises:
            FileNotFoundError: If data file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        if not self.data_file.exists():
            return create_empty_schema()

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all required keys exist
                if "notes" not in data:
                    data["notes"] = []
                if "tasks" not in data:
                    data["tasks"] = []
                if "courses" not in data:
                    data["courses"] = []
                return data
        except json.JSONDecodeError as e:
            # Try to recover from backup
            if self.bak_file.exists():
                with open(self.bak_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            raise ValueError(f"Corrupted data file: {e}") from e

    def save(self, data: DataSchema) -> None:
        """Save data to JSON file with atomic write.

        Process:
        1. Write to temporary file
        2. Create backup of existing file
        3. Rename temp file to target

        Args:
            data: Data schema to save
        """
        # Ensure parent directory exists
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to temporary file first
        with open(self.tmp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

        # Create backup if file exists
        if self.data_file.exists():
            shutil.copy2(self.data_file, self.bak_file)

        # Atomic rename
        self.tmp_file.replace(self.data_file)

    def backup_exists(self) -> bool:
        """Check if a backup file exists."""
        return self.bak_file.exists()

    def restore_from_backup(self) -> None:
        """Restore data from backup file.

        Raises:
            FileNotFoundError: If backup file doesn't exist
        """
        if not self.bak_file.exists():
            raise FileNotFoundError("No backup file found")
        shutil.copy2(self.bak_file, self.data_file)
