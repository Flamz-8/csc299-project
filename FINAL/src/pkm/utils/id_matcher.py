"""Utility for flexible ID matching to make IDs easier to work with."""


def find_matching_id(partial_id: str, available_ids: list[str]) -> str | None:
    """Find a matching ID from a partial ID input.

    Supports:
    - Exact match (case-insensitive)
    - Partial match from the beginning (e.g., "n1" matches "n1", "n_20251123_154149_4xl")
    - Unique suffix match (e.g., "4xl" matches "n_20251123_154149_4xl" if unique)

    Args:
        partial_id: The partial or full ID to match
        available_ids: List of available IDs to search

    Returns:
        The matched ID if found and unique, None otherwise

    Examples:
        >>> find_matching_id("n1", ["n1", "n2", "n10"])
        "n1"
        >>> find_matching_id("N1", ["n1", "n2"])
        "n1"
        >>> find_matching_id("4xl", ["n_20251123_154149_4xl", "t_20251123_154149_xyz"])
        "n_20251123_154149_4xl"
    """
    if not partial_id or not available_ids:
        return None

    partial_lower = partial_id.lower()

    # Try exact match (case-insensitive)
    for id_str in available_ids:
        if id_str.lower() == partial_lower:
            return id_str

    # Try prefix match
    prefix_matches = [id_str for id_str in available_ids if id_str.lower().startswith(partial_lower)]
    if len(prefix_matches) == 1:
        return prefix_matches[0]
    elif len(prefix_matches) > 1:
        # Multiple matches - not unique
        return None

    # Try suffix match (for timestamp-based IDs like n_20251123_154149_4xl)
    suffix_matches = [id_str for id_str in available_ids if id_str.lower().endswith(partial_lower)]
    if len(suffix_matches) == 1:
        return suffix_matches[0]

    # Try contains match (anywhere in the ID)
    contains_matches = [id_str for id_str in available_ids if partial_lower in id_str.lower()]
    if len(contains_matches) == 1:
        return contains_matches[0]

    return None


def get_match_suggestions(partial_id: str, available_ids: list[str], max_suggestions: int = 5) -> list[str]:
    """Get ID suggestions when a partial ID matches multiple IDs.

    Args:
        partial_id: The partial ID that was ambiguous
        available_ids: List of available IDs
        max_suggestions: Maximum number of suggestions to return

    Returns:
        List of matching IDs (up to max_suggestions)

    Examples:
        >>> get_match_suggestions("n1", ["n1", "n10", "n11", "n12"])
        ["n1", "n10", "n11", "n12"]
    """
    if not partial_id or not available_ids:
        return []

    partial_lower = partial_id.lower()

    # Find all IDs that contain the partial ID
    matches = [
        id_str
        for id_str in available_ids
        if partial_lower in id_str.lower()
    ]

    return matches[:max_suggestions]
