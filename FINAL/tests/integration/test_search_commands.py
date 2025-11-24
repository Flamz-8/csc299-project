"""Integration tests for search commands."""

from pathlib import Path

from click.testing import CliRunner

from pkm.cli.main import cli


class TestSearchCommands:
    """Integration tests for search functionality."""

    def test_search_finds_matching_items(self, temp_data_dir: Path) -> None:
        """Test US5-S1: Search finds notes and tasks matching query."""
        runner = CliRunner()

        # Add test data
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Photosynthesis in plants"],
        )

        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Study photosynthesis"],
        )

        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Mitochondria function"],
        )

        # Search for "photosynthesis"
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "search", "photosynthesis"],
        )

        assert result.exit_code == 0
        assert "Photosynthesis in plants" in result.output
        assert "Study photosynthesis" in result.output
        assert "Mitochondria" not in result.output

    def test_search_filtered_by_course(self, temp_data_dir: Path) -> None:
        """Test US5-S2: Search can filter by course."""
        runner = CliRunner()

        # Add items to different courses
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Biology exam notes",
                "--course", "Biology 101",
            ],
        )

        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Math exam notes",
                "--course", "Math 201",
            ],
        )

        # Search for "exam" in Biology course
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "search", "exam", "--course", "Biology 101"],
        )

        assert result.exit_code == 0
        assert "Biology exam notes" in result.output
        assert "Math exam notes" not in result.output

    def test_search_filtered_by_topic(self, temp_data_dir: Path) -> None:
        """Test US5-S3: Search can filter by topic."""
        runner = CliRunner()

        # Add notes with different topics
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Cell structure details",
                "--topics", "Cell Biology",
            ],
        )

        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "DNA replication",
                "--topics", "Genetics",
            ],
        )

        # Search with topic filter
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "search", "structure", "--topic", "Cell Biology"],
        )

        assert result.exit_code == 0
        assert "Cell structure details" in result.output

    def test_search_filtered_by_type(self, temp_data_dir: Path) -> None:
        """Test US5-S4: Search can filter by type (notes/tasks)."""
        runner = CliRunner()

        # Add note and task with same keyword
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Chapter 5 summary"],
        )

        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Read chapter 5"],
        )

        # Search only notes
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "search", "chapter", "--type", "notes"],
        )

        assert result.exit_code == 0
        assert "Chapter 5 summary" in result.output
        assert "Read chapter 5" not in result.output

    def test_search_no_results_shows_helpful_message(self, temp_data_dir: Path) -> None:
        """Test US5-S5: Search with no results shows helpful message."""
        runner = CliRunner()

        # Add some data
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Test data"],
        )

        # Search for non-existent term
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "search", "nonexistentterm12345"],
        )

        assert result.exit_code == 0
        assert "No results" in result.output or "not found" in result.output.lower() or "0 results" in result.output
