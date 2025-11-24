"""Integration tests for course management commands."""

from pathlib import Path

from click.testing import CliRunner

from pkm.cli.main import cli


class TestCourseCommands:
    """Integration tests for course commands."""

    def test_delete_course_moves_items_to_inbox(self, temp_data_dir: Path) -> None:
        """Test deleting a course moves its items to inbox by default."""
        runner = CliRunner()

        # Create items in a course
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Course note", "--course", "TestCourse"],
        )
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Course task", "--course", "TestCourse"],
        )

        # Delete course with confirmation
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "course", "delete", "TestCourse"],
            input="y\n",
        )

        assert result.exit_code == 0
        assert "deleted" in result.output.lower()
        assert "moved" in result.output.lower() or "1 notes" in result.output

        # Verify items are in inbox
        inbox_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "inbox"],
        )
        assert "Course note" in inbox_result.output
        assert "Course task" in inbox_result.output

    def test_delete_course_with_delete_items_flag(self, temp_data_dir: Path) -> None:
        """Test deleting a course and all its items."""
        runner = CliRunner()

        # Create items in a course
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Delete me note", "--course", "OldCourse"],
        )
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Delete me task", "--course", "OldCourse"],
        )

        # Delete course with --delete-items flag
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "course", "delete", "OldCourse", "--delete-items"],
            input="y\n",
        )

        assert result.exit_code == 0
        assert "deleted" in result.output.lower()
        assert "1 notes" in result.output and "1 tasks" in result.output

        # Verify items are gone (not in inbox)
        inbox_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "inbox"],
        )
        assert "Delete me note" not in inbox_result.output
        assert "Delete me task" not in inbox_result.output

    def test_delete_course_cancel_confirmation(self, temp_data_dir: Path) -> None:
        """Test cancelling course deletion at confirmation prompt."""
        runner = CliRunner()

        # Create course with items
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Keep me", "--course", "KeepCourse"],
        )

        # Cancel deletion
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "course", "delete", "KeepCourse"],
            input="n\n",
        )

        assert "cancel" in result.output.lower()

        # Verify course still exists by checking notes
        notes_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "notes", "--course", "KeepCourse"],
        )
        assert notes_result.exit_code == 0
        assert "Keep me" in notes_result.output

    def test_delete_course_with_yes_flag(self, temp_data_dir: Path) -> None:
        """Test deleting a course with --yes flag (skip confirmation)."""
        runner = CliRunner()

        # Create course
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Quick delete", "--course", "QuickCourse"],
        )

        # Delete with --yes flag
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "course", "delete", "QuickCourse", "-y"],
        )

        assert result.exit_code == 0
        assert "deleted" in result.output.lower()

    def test_delete_course_not_found(self, temp_data_dir: Path) -> None:
        """Test deleting a non-existent course."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "course", "delete", "NonExistentCourse", "-y"],
        )

        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_delete_course_empty(self, temp_data_dir: Path) -> None:
        """Test deleting a course with no items."""
        runner = CliRunner()

        # Create and immediately organize a note, then move it away
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Temp", "--course", "EmptyCourse"],
        )
        # Move the note to another course
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "organize", "note", "n1", "--course", "OtherCourse"],
        )

        # Now EmptyCourse should not exist anymore (no items)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "course", "delete", "EmptyCourse", "-y"],
        )

        # Should fail because course doesn't exist
        assert result.exit_code == 1
        assert "not found" in result.output.lower()
