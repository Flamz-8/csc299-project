"""Common types and ID generation for models."""



# Global counters for generating short IDs
_id_counters = {
    "n": 0,
    "t": 0,
    "c": 0,
}


def generate_id(prefix: str) -> str:
    """Generate a unique ID with format: {prefix}{number}.

    Args:
        prefix: Entity type prefix ('n' for note, 't' for task, 'c' for course)

    Returns:
        Unique ID string (e.g., "n1", "t5", "c2")

    Example:
        >>> id = generate_id("n")
        >>> id.startswith("n")
        True
    """
    # Get current max ID from storage to maintain uniqueness
    _id_counters[prefix] += 1
    return f"{prefix}{_id_counters[prefix]}"


def reset_id_counter(prefix: str, max_id: int) -> None:
    """Reset ID counter to the maximum existing ID.

    Args:
        prefix: Entity type prefix
        max_id: Maximum existing ID number
    """
    _id_counters[prefix] = max_id
