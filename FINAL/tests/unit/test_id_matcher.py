"""Unit tests for ID matcher utility."""

from pkm.utils.id_matcher import find_matching_id, get_match_suggestions


class TestIDMatcher:
    """Tests for flexible ID matching."""

    def test_exact_match(self) -> None:
        """Test exact ID match."""
        ids = ["n1", "n2", "n10"]
        assert find_matching_id("n1", ids) == "n1"
        assert find_matching_id("n2", ids) == "n2"
        assert find_matching_id("n10", ids) == "n10"

    def test_case_insensitive_match(self) -> None:
        """Test case-insensitive matching."""
        ids = ["n1", "n2", "N10"]
        assert find_matching_id("N1", ids) == "n1"
        assert find_matching_id("n2", ids) == "n2"
        assert find_matching_id("n10", ids) == "N10"

    def test_prefix_match(self) -> None:
        """Test prefix matching."""
        ids = ["n_20251123_154149_4xl", "n_20251123_155510_rw4", "n1"]
        assert find_matching_id("n_2025", ids) == None  # Matches multiple
        assert find_matching_id("n_20251123_154", ids) == "n_20251123_154149_4xl"
        assert find_matching_id("n1", ids) == "n1"

    def test_suffix_match(self) -> None:
        """Test suffix matching."""
        ids = ["n_20251123_154149_4xl", "n_20251123_155510_rw4", "t_20251123_154149_xyz"]
        assert find_matching_id("4xl", ids) == "n_20251123_154149_4xl"
        assert find_matching_id("rw4", ids) == "n_20251123_155510_rw4"
        assert find_matching_id("xyz", ids) == "t_20251123_154149_xyz"

    def test_contains_match(self) -> None:
        """Test contains matching."""
        ids = ["n_20251123_154149_4xl", "n_20251124_155510_rw4"]
        assert find_matching_id("154149", ids) == "n_20251123_154149_4xl"
        assert find_matching_id("20251124", ids) == "n_20251124_155510_rw4"

    def test_no_match(self) -> None:
        """Test when no match is found."""
        ids = ["n1", "n2", "n3"]
        assert find_matching_id("n10", ids) is None
        assert find_matching_id("t1", ids) is None
        assert find_matching_id("xyz", ids) is None

    def test_ambiguous_match(self) -> None:
        """Test ambiguous matches return None."""
        ids = ["n1", "n10", "n11", "n100"]
        assert find_matching_id("n1", ids) == "n1"  # Exact match takes precedence
        assert find_matching_id("1", ids) is None  # Matches multiple

    def test_empty_input(self) -> None:
        """Test with empty input."""
        assert find_matching_id("", ["n1", "n2"]) is None
        assert find_matching_id("n1", []) is None

    def test_get_suggestions(self) -> None:
        """Test getting match suggestions."""
        ids = ["n1", "n10", "n11", "n12", "n100"]
        suggestions = get_match_suggestions("n1", ids)
        assert len(suggestions) <= 5
        assert "n1" in suggestions
        assert "n10" in suggestions

    def test_get_suggestions_max_limit(self) -> None:
        """Test suggestions are limited to max."""
        ids = ["n1", "n10", "n11", "n12", "n13", "n14", "n15"]
        suggestions = get_match_suggestions("n1", ids, max_suggestions=3)
        assert len(suggestions) == 3

    def test_timestamp_based_ids(self) -> None:
        """Test with real timestamp-based IDs."""
        ids = [
            "n_20251123_154149_4xl",
            "n_20251123_155510_rw4",
            "t_20251123_154155_abc",
            "n1",
            "n2",
        ]
        assert find_matching_id("4xl", ids) == "n_20251123_154149_4xl"
        assert find_matching_id("rw4", ids) == "n_20251123_155510_rw4"
        assert find_matching_id("abc", ids) == "t_20251123_154155_abc"
        assert find_matching_id("n1", ids) == "n1"
        assert find_matching_id("n2", ids) == "n2"
