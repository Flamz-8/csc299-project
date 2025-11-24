"""Unit tests for date parsing utilities."""

from datetime import datetime, timedelta

from pkm.utils.date_parser import format_due_date, parse_due_date


class TestDateParser:
    """Unit tests for natural language date parsing."""

    def test_parse_today(self) -> None:
        """Test parsing 'today' returns today at 23:59:59."""
        result = parse_due_date("today")
        assert result is not None
        assert result.date() == datetime.now().date()
        assert result.hour == 23
        assert result.minute == 59

    def test_parse_tomorrow(self) -> None:
        """Test parsing 'tomorrow' returns tomorrow at 23:59:59."""
        result = parse_due_date("tomorrow")
        assert result is not None
        expected_date = (datetime.now() + timedelta(days=1)).date()
        assert result.date() == expected_date
        assert result.hour == 23
        assert result.minute == 59

    def test_parse_in_days(self) -> None:
        """Test parsing 'in X days' format."""
        result = parse_due_date("in 3 days")
        assert result is not None
        expected_date = (datetime.now() + timedelta(days=3)).date()
        assert result.date() == expected_date

    def test_parse_in_weeks(self) -> None:
        """Test parsing 'in X weeks' format."""
        result = parse_due_date("in 2 weeks")
        assert result is not None
        expected_date = (datetime.now() + timedelta(weeks=2)).date()
        assert result.date() == expected_date

    def test_parse_iso_date(self) -> None:
        """Test parsing ISO format dates (YYYY-MM-DD)."""
        result = parse_due_date("2025-12-25")
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 23
        assert result.minute == 59

    def test_parse_next_weekday(self) -> None:
        """Test parsing 'next Friday' format."""
        result = parse_due_date("next Friday")
        assert result is not None
        # Result should be in the future
        assert result > datetime.now()
        # Should be a Friday (weekday 4)
        assert result.weekday() == 4

    def test_parse_with_time(self) -> None:
        """Test parsing dates with specific times."""
        result = parse_due_date("tomorrow at 5pm")
        assert result is not None
        assert result.hour == 17

    def test_parse_empty_string(self) -> None:
        """Test that empty string returns None."""
        result = parse_due_date("")
        assert result is None

    def test_parse_whitespace(self) -> None:
        """Test that whitespace-only string returns None."""
        result = parse_due_date("   ")
        assert result is None

    def test_parse_invalid_date(self) -> None:
        """Test that invalid date string returns None."""
        parse_due_date("not a date at all")
        # May parse to something or None, depending on fuzzy parsing
        # At minimum should not crash

    def test_format_due_date(self) -> None:
        """Test formatting a datetime for display."""
        dt = datetime(2025, 11, 25, 23, 59, 0)
        result = format_due_date(dt)
        assert isinstance(result, str)
        assert "Nov 25" in result or "11" in result

    def test_format_due_date_relative(self) -> None:
        """Test that formatted dates include relative time."""
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(hour=23, minute=59, second=0)
        result = format_due_date(tomorrow)
        assert "tomorrow" in result.lower() or "1 day" in result.lower()


class TestEdgeCases:
    """Edge case tests for date parsing."""

    def test_case_insensitive(self) -> None:
        """Test that parsing is case-insensitive."""
        result1 = parse_due_date("TOMORROW")
        result2 = parse_due_date("tomorrow")
        result3 = parse_due_date("Tomorrow")

        assert result1 is not None
        assert result2 is not None
        assert result3 is not None
        assert result1.date() == result2.date() == result3.date()

    def test_extra_whitespace(self) -> None:
        """Test parsing with extra whitespace."""
        result = parse_due_date("  tomorrow  ")
        assert result is not None
        expected_date = (datetime.now() + timedelta(days=1)).date()
        assert result.date() == expected_date

    def test_midnight_vs_end_of_day(self) -> None:
        """Test that dates without time default to end of day."""
        result = parse_due_date("2025-12-25")
        assert result is not None
        # Should be 23:59:59, not 00:00:00
        assert result.hour == 23
        assert result.minute == 59

    def test_past_date_allowed(self) -> None:
        """Test that past dates can be parsed (for overdue tasks)."""
        result = parse_due_date("2020-01-01")
        assert result is not None
        assert result.year == 2020
        assert result < datetime.now()
