"""Note model definition."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Note(BaseModel):
    """A note capturing information, lecture notes, ideas, or references.

    Attributes:
        id: Unique identifier (e.g., "n1", "n42")
        content: Note body text (multi-line supported)
        created_at: Timestamp when note was created
        modified_at: Last modification timestamp
        course: Course assignment (None = inbox)
        topics: Topic tags for categorization
        linked_from_tasks: Task IDs that reference this note
    """

    id: str = Field(..., pattern=r"^n\d+$")
    content: str = Field(..., min_length=1, max_length=10000)
    created_at: datetime
    modified_at: datetime
    course: str | None = Field(None, min_length=1, max_length=100)
    topics: list[str] = Field(default_factory=list)
    linked_from_tasks: list[str] = Field(default_factory=list)

    @field_validator("topics")
    @classmethod
    def validate_topics(cls, v: list[str]) -> list[str]:
        """Validate that each topic is 1-50 characters."""
        for topic in v:
            if not topic or len(topic) > 50:
                raise ValueError("Each topic must be 1-50 characters")
        return v

    model_config = {"frozen": False}  # Allow modification of fields
