"""Data migration utilities for schema versioning."""

from typing import Any


def get_schema_version(data: dict[str, Any]) -> int:
    """Get the schema version from data.

    Args:
        data: JSON data dictionary

    Returns:
        Schema version (default: 1)
    """
    return data.get("_schema_version", 1)


def migrate_to_latest(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate data to the latest schema version.

    Args:
        data: JSON data dictionary

    Returns:
        Migrated data
    """
    current_version = get_schema_version(data)

    # No migrations needed yet - we're at version 1
    if current_version == 1:
        return data

    # Future migrations would go here:
    # if current_version < 2:
    #     data = migrate_v1_to_v2(data)
    # if current_version < 3:
    #     data = migrate_v2_to_v3(data)

    return data


def add_schema_version(data: dict[str, Any], version: int = 1) -> dict[str, Any]:
    """Add schema version to data.

    Args:
        data: JSON data dictionary
        version: Schema version number

    Returns:
        Data with schema version added
    """
    data["_schema_version"] = version
    return data
