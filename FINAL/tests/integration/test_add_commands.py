"""Integration tests for add commands."""

from pathlib import Path

from click.testing import CliRunner

from pkm.cli.main import cli


class TestAddCommands:
    """Integration tests for add commands."""

    def test_add_note_creates_in_inbox(self, temp_data_dir: Path) -> None:
        """Test US1-S1: Adding a note creates it in inbox with ID and timestamp."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Test note content"],
        )

        assert result.exit_code == 0
        assert "Note created:" in result.output
        assert "inbox" in result.output
        assert "n" in result.output  # Note ID format (n1, n2, etc.)

    def test_add_task_creates_in_inbox(self, temp_data_dir: Path) -> None:
        """Test US1-S2: Adding a task creates it in inbox."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Test task"],
        )

        assert result.exit_code == 0
        assert "Task created:" in result.output
        assert "inbox" in result.output
        assert "t" in result.output  # Task ID format (t1, t2, etc.)

    def test_add_note_with_topics(self, temp_data_dir: Path) -> None:
        """Test adding a note with topic tags."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Biology note",
                "--topics",
                "Photosynthesis",
                "--topics",
                "Cell Structure",
            ],
        )

        assert result.exit_code == 0
        assert "Tagged with: Photosynthesis, Cell Structure" in result.output

    def test_add_task_with_priority(self, temp_data_dir: Path) -> None:
        """Test adding a task with priority."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "task",
                "Important task",
                "--priority",
                "high",
            ],
        )

        assert result.exit_code == 0
        assert "Priority: high" in result.output

    def test_add_note_to_course(self, temp_data_dir: Path) -> None:
        """Test adding a note directly to a course."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Course note",
                "--course",
                "Biology 101",
            ],
        )

        assert result.exit_code == 0
        assert "course 'Biology 101'" in result.output
