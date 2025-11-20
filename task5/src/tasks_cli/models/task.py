"""Task model for representing task entities."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Task:
    """Represents a single task item.

    Attributes:
        id: Sequential integer identifier starting from 1
        description: Text content of the task (1-1000 characters)
        timestamp: ISO 8601 timestamp when task was created (UTC)
        status: Current status (only 'pending' in MVP, extensible)

    Example:
        >>> task = Task(
        ...     id=1,
        ...     description="Buy groceries",
        ...     timestamp="2025-11-19T10:30:00Z",
        ...     status="pending"
        ... )
    """

    id: int
    description: str
    timestamp: str  # ISO 8601 format
    status: Literal["pending"] = "pending"

    def __post_init__(self) -> None:
        """Validate task attributes after initialization."""
        if self.id < 1:
            msg = f"Task ID must be positive, got {self.id}"
            raise ValueError(msg)

        if not self.description or not self.description.strip():
            msg = "Task description cannot be empty"
            raise ValueError(msg)

        if len(self.description) > 1000:
            msg = (
                f"Task description too long ({len(self.description)} chars), "
                f"maximum is 1000 characters"
            )
            raise ValueError(msg)

        # Basic ISO 8601 format validation
        try:
            datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
        except ValueError as e:
            msg = (
                f"Invalid timestamp format: {self.timestamp}. "
                f"Expected ISO 8601 format (e.g., '2025-11-19T10:30:00Z')"
            )
            raise ValueError(msg) from e

    def to_dict(self) -> dict[str, str | int]:
        """Serialize to dictionary for JSON storage.

        Returns:
            Dictionary with id, description, timestamp, and status keys.
        """
        return {
            "id": self.id,
            "description": self.description,
            "timestamp": self.timestamp,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> "Task":
        """Deserialize from dictionary.

        Args:
            data: Dictionary with task data.

        Returns:
            Task instance created from dictionary data.
        """
        return cls(
            id=int(data["id"]),
            description=str(data["description"]),
            timestamp=str(data["timestamp"]),
            status=str(data.get("status", "pending")),  # type: ignore[arg-type]
        )
