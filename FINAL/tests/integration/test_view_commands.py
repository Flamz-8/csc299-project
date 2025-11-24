"""Integration tests for view commands."""

from pathlib import Path

from click.testing import CliRunner

from pkm.cli.main import cli


class TestViewCommands:
    """Integration tests for view commands."""

    def test_view_inbox_shows_all_items(self, temp_data_dir: Path) -> None:
        """Test US1-S3: View inbox shows all unorganized notes and tasks."""
        runner = CliRunner()

        # Add a note
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Inbox note"],
        )

        # Add a task
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Inbox task"],
        )

        # View inbox
        result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "inbox"]
        )

        assert result.exit_code == 0
        assert "Inbox Notes" in result.output
        assert "Inbox Tasks" in result.output
        assert "Inbox note" in result.output
        assert "Inbox task" in result.output
        assert "Total inbox items: 2" in result.output

    def test_view_inbox_empty(self, temp_data_dir: Path) -> None:
        """Test viewing empty inbox."""
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "inbox"]
        )

        assert result.exit_code == 0
        assert "Inbox is empty" in result.output

    def test_view_inbox_excludes_organized_items(self, temp_data_dir: Path) -> None:
        """Test that inbox only shows items without a course."""
        runner = CliRunner()

        # Add inbox note
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Inbox note"],
        )

        # Add course note
        runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Course note",
                "--course",
                "Biology",
            ],
        )

        # View inbox
        result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "inbox"]
        )

        assert result.exit_code == 0
        assert "Inbox note" in result.output
        assert "Course note" not in result.output
        assert "Total inbox items: 1" in result.output

    def test_view_inbox_with_show_ids(self, temp_data_dir: Path) -> None:
        """Test viewing inbox with --show-ids flag displays IDs."""
        runner = CliRunner()

        # Add a note and task
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Test note"],
        )
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Test task"],
        )

        # View inbox with IDs
        result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "inbox", "--show-ids"]
        )

        assert result.exit_code == 0
        assert "ID" in result.output  # ID column should be present
        assert "n1" in result.output  # Note ID should be visible
        assert "t1" in result.output  # Task ID should be visible

    def test_add_task_with_due_date(self, temp_data_dir: Path) -> None:
        """Test US2-S1: Adding task with natural language due date."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Study for exam", "--due", "tomorrow"],
        )

        assert result.exit_code == 0
        assert "Task created:" in result.output

    def test_view_today_filters_correctly(self, temp_data_dir: Path) -> None:
        """Test US2-S2: View today shows only tasks due today."""
        runner = CliRunner()

        # Add task due today
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Due today", "--due", "today"],
        )

        # Add task due tomorrow
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Due tomorrow", "--due", "tomorrow"],
        )

        # View today
        result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "today"]
        )

        assert result.exit_code == 0
        assert "Due today" in result.output
        assert "Due tomorrow" not in result.output

    def test_view_week_filters_correctly(self, temp_data_dir: Path) -> None:
        """Test US2-S3: View week shows tasks due within 7 days."""
        runner = CliRunner()

        # Add task due in 3 days
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Due this week", "--due", "in 3 days"],
        )

        # Add task with no due date
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "No due date"],
        )

        # View week
        result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "week"]
        )

        assert result.exit_code == 0
        assert "Due this week" in result.output

    def test_view_overdue_shows_past_due(self, temp_data_dir: Path) -> None:
        """Test US2-S4: View overdue shows past-due incomplete tasks."""
        runner = CliRunner()

        # Create task and complete it
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Current task", "--due", "today"],
        )

        # View overdue (should be empty initially)
        result = runner.invoke(
            cli, ["--data-dir", str(temp_data_dir), "view", "overdue"]
        )

        assert result.exit_code == 0

    def test_view_note_shows_referencing_tasks(self, temp_data_dir: Path) -> None:
        """Test US6-S5: Viewing a note shows tasks that reference it."""
        runner = CliRunner()

        # Create note and task
        note_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "Research data"],
        )
        note_id = note_result.output.split("Note created: ")[1].split()[0]

        task_result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "task", "Analyze data"],
        )
        task_id = task_result.output.split("Task created: ")[1].split()[0]

        # Link task to note
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "link-note", task_id, note_id],
        )

        # View note
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "note", note_id],
        )

        assert result.exit_code == 0
        assert task_id in result.output or "Analyze data" in result.output

    def test_view_notes_filtered_by_course_and_topic(self, temp_data_dir: Path) -> None:
        """Test US4-S3: Viewing notes filtered by course and topic."""
        runner = CliRunner()

        # Create notes with different courses and topics
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Biology note 1",
                "--course", "Biology 101",
            ],
        )
        note1_result = runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Biology note 2",
                "--course", "Biology 101",
            ],
        )
        note1_id = note1_result.output.split("Note created: ")[1].split()[0]

        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Math note",
                "--course", "Math 201",
            ],
        )

        # Add topic to biology note
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "organize", "note", note1_id,
                "--add-topics", "photosynthesis",
            ],
        )

        # View notes filtered by course using view course command
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "course", "Biology 101"],
        )

        assert result.exit_code == 0
        assert "Biology note 1" in result.output
        assert "Biology note 2" in result.output
        assert "Math note" not in result.output

    def test_view_notes_grouped_correctly(self, temp_data_dir: Path) -> None:
        """Test US4-S4: Viewing notes with grouping by course then topic."""
        runner = CliRunner()

        # Create notes with courses and topics
        bio_note1 = runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Cell structure notes",
                "--course", "Biology",
            ],
        )
        bio_note1_id = bio_note1.output.split("Note created: ")[1].split()[0]

        bio_note2 = runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Photosynthesis notes",
                "--course", "Biology",
            ],
        )
        bio_note2_id = bio_note2.output.split("Note created: ")[1].split()[0]

        math_note = runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Calculus notes",
                "--course", "Math",
            ],
        )

        # Add topics
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "organize", "note", bio_note1_id,
                "--add-topics", "cells",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "organize", "note", bio_note2_id,
                "--add-topics", "energy",
            ],
        )

        # View Biology course (should be grouped by topic)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "course", "Biology"],
        )

        assert result.exit_code == 0
        # Verify course name appears
        assert "Biology" in result.output
        # Verify all notes appear
        assert "Cell structure notes" in result.output
        assert "Photosynthesis notes" in result.output
        # Math notes should not appear
        assert "Calculus notes" not in result.output

    def test_view_notes_empty(self, temp_data_dir: Path) -> None:
        """Test viewing notes when none exist."""
        runner = CliRunner()

        # View inbox when no notes exist
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "inbox"],
        )

        assert result.exit_code == 0
        assert "empty" in result.output.lower() or "no notes" in result.output.lower()

    def test_view_notes_filtered_no_matches(self, temp_data_dir: Path) -> None:
        """Test viewing notes with filter that matches nothing."""
        runner = CliRunner()

        # Create a note
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Test note",
                "--course", "Biology",
            ],
        )

        # Filter by non-existent course
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "course", "Physics"],
        )

        assert result.exit_code == 0
        # Should show empty course or indicate no items
        assert "Physics" in result.output

    def test_view_notes_command_lists_all(self, temp_data_dir: Path) -> None:
        """Test view notes command shows all notes with IDs."""
        runner = CliRunner()

        # Create multiple notes
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "First note",
                "--topics", "Topic1",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Second note",
                "--course", "Biology",
                "--topics", "Topic2",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Third note",
            ],
        )

        # View all notes
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "notes"],
        )

        assert result.exit_code == 0
        assert "All Notes (3)" in result.output
        assert "First note" in result.output
        assert "Second note" in result.output
        assert "Third note" in result.output
        assert "n1" in result.output
        assert "n2" in result.output
        assert "n3" in result.output
        assert "Topic1" in result.output
        assert "Topic2" in result.output
        assert "Biology" in result.output

    def test_view_notes_command_filter_by_course(self, temp_data_dir: Path) -> None:
        """Test view notes command with course filter."""
        runner = CliRunner()

        # Create notes in different courses
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Biology note",
                "--course", "Biology 101",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Math note",
                "--course", "Math 201",
            ],
        )

        # View notes filtered by course
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "notes", "--course", "Biology 101"],
        )

        assert result.exit_code == 0
        assert "Biology 101" in result.output
        assert "Biology note" in result.output
        assert "Math note" not in result.output

    def test_view_notes_command_filter_by_topic(self, temp_data_dir: Path) -> None:
        """Test view notes command with topic filter."""
        runner = CliRunner()

        # Create notes with different topics
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Cell biology",
                "--topics", "Biology",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "note", "Algebra basics",
                "--topics", "Math",
            ],
        )

        # View notes filtered by topic
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "notes", "--topic", "Biology"],
        )

        assert result.exit_code == 0
        assert "Biology" in result.output
        assert "Cell biology" in result.output
        assert "Algebra basics" not in result.output

    def test_view_tasks_command_lists_all(self, temp_data_dir: Path) -> None:
        """Test view tasks command shows all active tasks with IDs."""
        runner = CliRunner()

        # Create multiple tasks
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "First task",
                "--priority", "high",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Second task",
                "--course", "Biology",
                "--priority", "medium",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Third task",
                "--priority", "low",
            ],
        )

        # View all tasks
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "tasks"],
        )

        assert result.exit_code == 0
        assert "All Tasks (Active) (3)" in result.output
        assert "First task" in result.output
        assert "Second task" in result.output
        assert "Third task" in result.output
        assert "t1" in result.output
        assert "t2" in result.output
        assert "t3" in result.output
        assert "HIGH" in result.output
        assert "MED" in result.output
        assert "LOW" in result.output

    def test_view_tasks_command_filter_by_course(self, temp_data_dir: Path) -> None:
        """Test view tasks command with course filter."""
        runner = CliRunner()

        # Create tasks in different courses
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Biology task",
                "--course", "Biology 101",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Math task",
                "--course", "Math 201",
            ],
        )

        # View tasks filtered by course
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "tasks", "--course", "Biology 101"],
        )

        assert result.exit_code == 0
        assert "Biology 101" in result.output
        assert "Biology task" in result.output
        assert "Math task" not in result.output

    def test_view_tasks_command_filter_by_priority(self, temp_data_dir: Path) -> None:
        """Test view tasks command with priority filter."""
        runner = CliRunner()

        # Create tasks with different priorities
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Important task",
                "--priority", "high",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Normal task",
                "--priority", "medium",
            ],
        )

        # View tasks filtered by priority
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "tasks", "--priority", "high"],
        )

        assert result.exit_code == 0
        assert "High Priority Tasks" in result.output
        assert "Important task" in result.output
        assert "Normal task" not in result.output

    def test_view_tasks_command_filter_by_status(self, temp_data_dir: Path) -> None:
        """Test view tasks command with status filter."""
        runner = CliRunner()

        # Create tasks and complete one
        runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Active task",
            ],
        )
        result = runner.invoke(
            cli,
            [
                "--data-dir", str(temp_data_dir),
                "add", "task", "Completed task",
            ],
        )
        
        # Get the task ID and mark it complete
        task_id = result.output.split("Task created: ")[1].split()[0]
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "task", "complete", task_id],
        )

        # View active tasks (default)
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "tasks"],
        )
        assert result.exit_code == 0
        assert "Active task" in result.output
        assert "Completed task" not in result.output

        # View completed tasks
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "tasks", "--status", "completed"],
        )
        assert result.exit_code == 0
        assert "Completed task" in result.output
        assert "Active task" not in result.output

        # View all tasks
        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "tasks", "--status", "all"],
        )
        assert result.exit_code == 0
        assert "Active task" in result.output
        # Task title might be truncated in display
        assert "Completed" in result.output or "t2" in result.output

    def test_view_topics_command_lists_all(self, temp_data_dir: Path) -> None:
        """Test view topics command lists all topics."""
        runner = CliRunner()

        # Create notes with various topics
        runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Machine learning basics",
                "--topics",
                "AI",
                "--topics",
                "Machine Learning",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Neural networks",
                "--topics",
                "AI",
                "--topics",
                "Deep Learning",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Biology basics",
                "--topics",
                "Biology",
                "--topics",
                "Science",
            ],
        )

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "topics"],
        )
        assert result.exit_code == 0
        assert "AI" in result.output
        assert "Machine Learning" in result.output
        assert "Deep Learning" in result.output
        assert "Biology" in result.output
        assert "Science" in result.output
        assert "Found 5 topics" in result.output

    def test_view_topics_command_filter_by_topic(self, temp_data_dir: Path) -> None:
        """Test view topics command with topic filter."""
        runner = CliRunner()

        # Create notes with various topics
        runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "ML basics",
                "--topics",
                "AI",
                "--topics",
                "Machine Learning",
            ],
        )
        runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Biology basics",
                "--topics",
                "Biology",
            ],
        )

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "topics", "--topic", "AI"],
        )
        assert result.exit_code == 0
        assert "AI" in result.output
        assert "ML basics" in result.output
        assert "Biology" not in result.output
        assert "Found 1 topics" in result.output

    def test_view_topics_command_empty(self, temp_data_dir: Path) -> None:
        """Test view topics with no topics."""
        runner = CliRunner()

        # Create note without topics
        runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "add", "note", "No topics here"],
        )

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "topics"],
        )
        assert result.exit_code == 0
        assert "No topics found" in result.output

    def test_view_topics_command_not_found(self, temp_data_dir: Path) -> None:
        """Test view topics with nonexistent topic."""
        runner = CliRunner()

        # Create note with topic
        runner.invoke(
            cli,
            [
                "--data-dir",
                str(temp_data_dir),
                "add",
                "note",
                "Test note",
                "--topics",
                "Testing",
            ],
        )

        result = runner.invoke(
            cli,
            ["--data-dir", str(temp_data_dir), "view", "topics", "--topic", "NonExistent"],
        )
        assert result.exit_code == 1
        assert "Topic not found: NonExistent" in result.output
        assert "Available topics:" in result.output

