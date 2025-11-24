"""Integration tests for note commands (US4)."""

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from pkm.cli.main import cli


class TestNoteCommands:
    """Integration tests for note management commands."""

    def test_edit_note_opens_editor(self, temp_data_dir: Path) -> None:
        """Test US4-S2: Editing a note opens external editor."""
        runner = CliRunner()

        # Create a note
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Original content"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        # Mock the editor to return edited content
        # Need to patch where it's used (in note.py), not where it's defined
        with patch("pkm.cli.note.open_in_editor") as mock_editor:
            mock_editor.return_value = "Edited content with changes"

            # Edit the note
            result = runner.invoke(
                cli,
                ["--data-dir", str(temp_data_dir), "note", "edit", note_id],
            )

            assert result.exit_code == 0
            assert "updated" in result.output.lower() or "saved" in result.output.lower()
            assert note_id in result.output

            # Verify the editor was called with original content
            mock_editor.assert_called_once_with("Original content")

        # Verify the note was updated by viewing it
        view_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "note", note_id],
        )
        assert view_result.exit_code == 0
        assert "Edited content with changes" in view_result.output

    def test_edit_note_no_changes(self, temp_data_dir: Path) -> None:
        """Test editing a note but not making changes."""
        runner = CliRunner()

        # Create a note
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Original content"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        # Mock the editor to return None (editor was closed without saving)
        with patch("pkm.cli.note.open_in_editor") as mock_editor:
            # When open_in_editor returns None, it means no edits were saved
            mock_editor.return_value = None

            # Edit the note
            result = runner.invoke(
                cli,
                ["--data-dir", str(temp_data_dir), "note", "edit", note_id],
            )

            # The command should indicate no changes
            # Note: ctx.exit() in Click may raise SystemExit which CliRunner catches
            assert "no changes" in result.output.lower() or "warning" in result.output.lower()

    def test_edit_note_not_found(self, temp_data_dir: Path) -> None:
        """Test editing a non-existent note."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "note", "edit", "n999"],
        )

        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_delete_note_with_confirmation(self, temp_data_dir: Path) -> None:
        """Test US4-S5: Deleting a note with confirmation prompt."""
        runner = CliRunner()

        # Create a note
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Note to delete"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        # Delete with confirmation (user says yes)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "note", "delete", note_id],
            input="y\n",
        )

        assert result.exit_code == 0
        assert "deleted" in result.output.lower()
        assert note_id in result.output

        # Verify the note is gone by trying to view it
        view_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "note", note_id],
        )
        assert view_result.exit_code == 1
        assert "not found" in view_result.output.lower()

    def test_delete_note_cancel_confirmation(self, temp_data_dir: Path) -> None:
        """Test canceling note deletion when prompted."""
        runner = CliRunner()

        # Create a note
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Note to keep"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        # Delete with confirmation (user says no)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "note", "delete", note_id],
            input="n\n",
        )

        # When user declines confirmation, the message should indicate cancellation
        assert "cancel" in result.output.lower() or "abort" in result.output.lower()

        # Verify the note still exists by trying to view it
        view_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "note", note_id],
        )
        assert view_result.exit_code == 0
        assert "Note to keep" in view_result.output

    def test_delete_note_with_force_flag(self, temp_data_dir: Path) -> None:
        """Test deleting a note with --yes flag (no confirmation)."""
        runner = CliRunner()

        # Create a note
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Force delete"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        # Delete with yes flag (no confirmation needed)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "note", "delete", note_id, "--yes"],
        )

        assert result.exit_code == 0
        assert "deleted" in result.output.lower()

        # Verify the note is gone
        view_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "note", note_id],
        )
        assert view_result.exit_code == 1

    def test_delete_note_linked_to_tasks(self, temp_data_dir: Path) -> None:
        """Test deleting a note that has linked tasks (should warn)."""
        runner = CliRunner()

        # Create a note and task
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Linked note"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Linked task"],
        )
        assert task_result.exit_code == 0
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        # Link task to note
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "link-note", task_id, note_id],
        )

        # Delete note (should show warning about linked tasks)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "note", "delete", note_id],
            input="y\n",
        )

        assert result.exit_code == 0
        assert "linked" in result.output.lower() or "reference" in result.output.lower()

    def test_delete_note_not_found(self, temp_data_dir: Path) -> None:
        """Test deleting a non-existent note."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "note", "delete", "n999", "--yes"],
        )

        assert result.exit_code == 1
        assert "not found" in result.output.lower()
