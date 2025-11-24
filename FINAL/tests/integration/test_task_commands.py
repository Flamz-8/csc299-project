"""Integration tests for task management commands."""

from pathlib import Path

from click.testing import CliRunner

from pkm.cli.main import cli


class TestTaskCommands:
    """Integration tests for task commands."""

    def test_task_complete_marks_done(self, temp_data_dir: Path) -> None:
        """Test US2-S5: Completing a task marks it done with timestamp."""
        runner = CliRunner()

        # Create a task first
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Test task"],
        )
        assert result.exit_code == 0

        # Extract task ID from output (e.g., "✓ Task created: t1 in inbox")
        task_id = result.output.split("Task created: ")[1].split()[0]

        # Complete the task
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "complete", task_id],
        )

        assert result.exit_code == 0
        assert "completed" in result.output.lower()
        assert "Test task" in result.output

    def test_link_note_to_task(self, temp_data_dir: Path) -> None:
        """Test US6-S1: Linking a note to a task creates bidirectional reference."""
        runner = CliRunner()

        # Create a note and a task
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Research findings"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Write report"],
        )
        assert task_result.exit_code == 0
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        # Link note to task
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "link-note", task_id, note_id],
        )

        assert result.exit_code == 0
        assert "linked" in result.output.lower()

    def test_view_task_shows_linked_notes(self, temp_data_dir: Path) -> None:
        """Test US6-S2: Viewing a task shows its linked notes."""
        runner = CliRunner()

        # Create note and task
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Important reference"],
        )
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Complete assignment"],
        )
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        # Link them
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "link-note", task_id, note_id],
        )

        # View task
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "task", task_id],
        )

        assert result.exit_code == 0
        assert "Linked Notes" in result.output or "linked" in result.output.lower()
        assert note_id in result.output

    def test_view_task_expand_shows_note_content(self, temp_data_dir: Path) -> None:
        """Test US6-S3: Viewing task with --expand shows full note content."""
        runner = CliRunner()

        note_content = "Detailed research findings about photosynthesis"

        # Create note and task
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", note_content],
        )
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Write lab report"],
        )
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        # Link and view with expand
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "link-note", task_id, note_id],
        )

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "task", task_id, "--expand"],
        )

        assert result.exit_code == 0
        assert note_content in result.output

    def test_unlink_note_from_task(self, temp_data_dir: Path) -> None:
        """Test US6-S4: Unlinking a note removes bidirectional reference."""
        runner = CliRunner()

        # Create and link
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Reference material"],
        )
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Research task"],
        )
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "link-note", task_id, note_id],
        )

        # Unlink
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "unlink-note", task_id, note_id],
        )

        assert result.exit_code == 0
        assert "unlinked" in result.output.lower() or "removed" in result.output.lower()

    def test_add_task_with_high_priority(self, temp_data_dir: Path) -> None:
        """Test US7-S1: Creating task with priority level."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Urgent assignment", "--priority", "high"],
        )

        assert result.exit_code == 0
        assert "Task created:" in result.output

    def test_add_subtask_to_task(self, temp_data_dir: Path) -> None:
        """Test US7-S2: Adding subtasks to break down work."""
        runner = CliRunner()

        # Create parent task
        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Complex project"],
        )
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        # Add subtask
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "add-subtask", task_id, "Step 1: Research"],
        )

        assert result.exit_code == 0
        assert "subtask" in result.output.lower() or "added" in result.output.lower()

    def test_complete_subtask(self, temp_data_dir: Path) -> None:
        """Test US7-S4: Marking a subtask as complete."""
        runner = CliRunner()

        # Create task and subtask
        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Project with steps"],
        )
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "add-subtask", task_id, "First step"],
        )

        # Complete the subtask (ID 1)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "check-subtask", task_id, "1"],
        )

        assert result.exit_code == 0
        assert "completed" in result.output.lower() or "checked" in result.output.lower()
