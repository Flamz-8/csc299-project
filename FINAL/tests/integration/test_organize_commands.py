"""Integration tests for organize commands."""

from pathlib import Path

from click.testing import CliRunner

from pkm.cli.main import cli


class TestOrganizeCommands:
    """Integration tests for organization commands."""

    def test_organize_note_moves_to_course(self, temp_data_dir: Path) -> None:
        """Test US3-S1: Organizing a note assigns it to a course."""
        runner = CliRunner()

        # Create a note in inbox
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Lecture notes on photosynthesis"],
        )
        assert note_result.exit_code == 0
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        # Organize to course
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "organize", "note", note_id, "--course", "Biology 101"],
        )

        assert result.exit_code == 0
        assert "organized" in result.output.lower() or "moved" in result.output.lower()
        assert "Biology 101" in result.output

    def test_organize_task_moves_to_course(self, temp_data_dir: Path) -> None:
        """Test organizing a task to a course."""
        runner = CliRunner()

        # Create a task in inbox
        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Complete problem set"],
        )
        assert task_result.exit_code == 0
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        # Organize to course
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "organize", "task", task_id, "--course", "Math 201"],
        )

        assert result.exit_code == 0
        assert "organized" in result.output.lower() or "moved" in result.output.lower()
        assert "Math 201" in result.output

    def test_organize_note_adds_topics(self, temp_data_dir: Path) -> None:
        """Test US4-S1: Organizing can add topics to notes."""
        runner = CliRunner()

        # Create note
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Cell biology notes"],
        )
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        # Organize with topics
        result = runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "organize", "note", note_id,
                "--course", "Biology 101",
                "--add-topics", "Cell Structure",
                "--add-topics", "Organelles",
            ],
        )

        assert result.exit_code == 0
        assert "organized" in result.output.lower() or "moved" in result.output.lower()

    def test_add_task_directly_to_course(self, temp_data_dir: Path) -> None:
        """Test US3-S2: Adding task directly to course (bypass inbox)."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Read chapter 5",
                "--course", "History 301",
            ],
        )

        assert result.exit_code == 0
        assert "Task created:" in result.output

        # Verify it's not in inbox
        inbox_result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "inbox"]
        )
        assert "Read chapter 5" not in inbox_result.output or "Inbox is empty" in inbox_result.output

    def test_view_course_shows_all_items(self, temp_data_dir: Path) -> None:
        """Test US3-S3: Viewing a course shows all its notes and tasks."""
        runner = CliRunner()

        # Add note to course
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Course lecture notes",
                "--course", "Biology 101",
            ],
        )

        # Add task to course
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Course assignment",
                "--course", "Biology 101",
            ],
        )

        # View course
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "course", "Biology 101"],
        )

        assert result.exit_code == 0
        assert "Biology 101" in result.output
        assert "Course lecture notes" in result.output
        assert "Course assignment" in result.output

    def test_list_courses_shows_all(self, temp_data_dir: Path) -> None:
        """Test US3-S5: Listing all courses with item counts."""
        runner = CliRunner()

        # Add items to multiple courses
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Bio note",
                "--course", "Biology",
            ],
        )

        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Math homework",
                "--course", "Math",
            ],
        )

        # List courses
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "courses"],
        )

        assert result.exit_code == 0
        assert "Biology" in result.output
        assert "Math" in result.output
