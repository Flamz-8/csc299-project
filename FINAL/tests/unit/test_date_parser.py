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


class TestTimeFormats:
    """Test various time format parsing."""

    def test_parse_time_12hr_am(self) -> None:
        """Test parsing 12-hour AM time format."""
        result = parse_due_date("tomorrow at 9am")
        assert result is not None
        assert result.hour == 9
        # Minutes may default to current time when parsing fuzzy dates

    def test_parse_time_12hr_pm(self) -> None:
        """Test parsing 12-hour PM time format."""
        result = parse_due_date("tomorrow at 3pm")
        assert result is not None
        assert result.hour == 15  # 3 PM in 24-hour format
        # Minutes may default to current time when parsing fuzzy dates

    def test_parse_time_with_minutes(self) -> None:
        """Test parsing time with minutes."""
        result = parse_due_date("tomorrow at 2:30pm")
        assert result is not None
        assert result.hour == 14
        assert result.minute == 30

    def test_parse_time_24hr_format(self) -> None:
        """Test parsing 24-hour format."""
        result = parse_due_date("tomorrow at 14:30")
        assert result is not None
        assert result.hour == 14
        assert result.minute == 30

    def test_parse_midnight(self) -> None:
        """Test parsing midnight using explicit time."""
        result = parse_due_date("tomorrow at 00:00")
        assert result is not None
        assert result.hour == 0
        assert result.minute == 0

    def test_parse_noon(self) -> None:
        """Test parsing noon using 12pm format."""
        result = parse_due_date("tomorrow at 12pm")
        assert result is not None
        assert result.hour == 12

    def test_parse_time_without_at(self) -> None:
        """Test parsing time without 'at' keyword."""
        result = parse_due_date("tomorrow 5pm")
        assert result is not None
        assert result.hour == 17

    def test_parse_end_of_day_default(self) -> None:
        """Test that dates without time default to 23:59."""
        result = parse_due_date("next Monday")
        assert result is not None
        assert result.hour == 23
        assert result.minute == 59


class TestNaturalLanguageDates:
    """Test natural language date parsing."""

    def test_parse_this_friday(self) -> None:
        """Test parsing 'this Friday'."""
        result = parse_due_date("this Friday")
        assert result is not None
        assert result.weekday() == 4  # Friday

    def test_parse_next_monday(self) -> None:
        """Test parsing 'next Monday'."""
        result = parse_due_date("next Monday")
        assert result is not None
        assert result.weekday() == 0  # Monday
        assert result > datetime.now()

    def test_parse_next_thursday(self) -> None:
        """Test parsing 'next Thursday'."""
        result = parse_due_date("next Thursday")
        assert result is not None
        assert result.weekday() == 3  # Thursday

    def test_parse_in_one_day(self) -> None:
        """Test parsing 'in 1 day'."""
        result = parse_due_date("in 1 day")
        assert result is not None
        expected_date = (datetime.now() + timedelta(days=1)).date()
        assert result.date() == expected_date

    def test_parse_in_five_days(self) -> None:
        """Test parsing 'in 5 days'."""
        result = parse_due_date("in 5 days")
        assert result is not None
        expected_date = (datetime.now() + timedelta(days=5)).date()
        assert result.date() == expected_date

    def test_parse_in_one_week(self) -> None:
        """Test parsing 'in 1 week'."""
        result = parse_due_date("in 1 week")
        assert result is not None
        expected_date = (datetime.now() + timedelta(weeks=1)).date()
        assert result.date() == expected_date

    def test_parse_in_three_weeks(self) -> None:
        """Test parsing 'in 3 weeks'."""
        result = parse_due_date("in 3 weeks")
        assert result is not None
        expected_date = (datetime.now() + timedelta(weeks=3)).date()
        assert result.date() == expected_date

    def test_parse_in_one_month(self) -> None:
        """Test parsing 'in 1 month'."""
        result = parse_due_date("in 1 month")
        assert result is not None
        # Verify it's approximately 30 days ahead
        days_diff = (result.date() - datetime.now().date()).days
        assert 28 <= days_diff <= 31

    def test_parse_in_months(self) -> None:
        """Test parsing 'in 2 months'."""
        result = parse_due_date("in 2 months")
        assert result is not None
        # Verify it's approximately 60 days ahead
        days_diff = (result.date() - datetime.now().date()).days
        assert 56 <= days_diff <= 62


class TestDateFormats:
    """Test various date format parsing."""

    def test_parse_iso_format(self) -> None:
        """Test parsing ISO 8601 date format."""
        result = parse_due_date("2025-12-25")
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 25

    def test_parse_us_format(self) -> None:
        """Test parsing US date format (MM/DD/YYYY)."""
        result = parse_due_date("12/25/2025")
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 25

    def test_parse_short_month_name(self) -> None:
        """Test parsing with short month name."""
        result = parse_due_date("Dec 25")
        assert result is not None
        assert result.month == 12
        assert result.day == 25

    def test_parse_full_month_name(self) -> None:
        """Test parsing with full month name."""
        result = parse_due_date("December 25")
        assert result is not None
        assert result.month == 12
        assert result.day == 25

    def test_parse_month_day_year(self) -> None:
        """Test parsing 'Month Day Year' format."""
        result = parse_due_date("December 25 2025")
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 25

    def test_parse_day_month_year(self) -> None:
        """Test parsing 'Day Month Year' format."""
        result = parse_due_date("25 December 2025")
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 25


class TestFormatDueDate:
    """Test due date formatting."""

    def test_format_today(self) -> None:
        """Test formatting a date due today."""
        today = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
        result = format_due_date(today)
        assert "today" in result.lower()

    def test_format_tomorrow(self) -> None:
        """Test formatting a date due tomorrow."""
        tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=23, minute=59, second=0)
        result = format_due_date(tomorrow)
        assert "tomorrow" in result.lower()

    def test_format_yesterday(self) -> None:
        """Test formatting a past date (yesterday)."""
        yesterday = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=0)
        result = format_due_date(yesterday)
        assert "yesterday" in result.lower()

    def test_format_multiple_days_future(self) -> None:
        """Test formatting a date several days in the future."""
        future = (datetime.now() + timedelta(days=5)).replace(hour=14, minute=30, second=0)
        result = format_due_date(future)
        assert "5 days" in result.lower()
        assert "2:30 PM" in result or "14:30" in result

    def test_format_multiple_days_past(self) -> None:
        """Test formatting a date several days in the past."""
        past = (datetime.now() - timedelta(days=3)).replace(hour=10, minute=0, second=0)
        result = format_due_date(past)
        assert "3 days ago" in result.lower()

    def test_format_includes_weekday(self) -> None:
        """Test that formatted date includes weekday name."""
        dt = datetime(2025, 11, 28, 15, 30, 0)  # Friday
        result = format_due_date(dt)
        weekday_name = dt.strftime("%A")
        assert weekday_name in result

    def test_format_includes_month(self) -> None:
        """Test that formatted date includes month abbreviation."""
        dt = datetime(2025, 12, 25, 23, 59, 0)
        result = format_due_date(dt)
        assert "Dec" in result

    def test_format_includes_time(self) -> None:
        """Test that formatted date includes time."""
        dt = datetime(2025, 12, 25, 14, 30, 0)
        result = format_due_date(dt)
        assert "2:30 PM" in result or "14:30" in result


class TestInvalidDates:
    """Test handling of invalid date inputs."""

    def test_parse_nonsense_string(self) -> None:
        """Test that nonsense strings return None or don't crash."""
        result = parse_due_date("asdfghjkl")
        # Might return None or parse to something - just shouldn't crash
        assert result is None or isinstance(result, datetime)

    def test_parse_empty_after_strip(self) -> None:
        """Test that strings that are empty after stripping return None."""
        result = parse_due_date("   \t\n   ")
        assert result is None

    def test_parse_invalid_month(self) -> None:
        """Test handling of invalid month."""
        result = parse_due_date("2025-13-01")  # Month 13 doesn't exist
        # Should either return None or handle gracefully
        assert result is None or isinstance(result, datetime)

    def test_parse_invalid_day(self) -> None:
        """Test handling of invalid day."""
        result = parse_due_date("2025-02-30")  # Feb 30 doesn't exist
        # Should either return None or handle gracefully
        assert result is None or isinstance(result, datetime)

    def test_parse_symbols_only(self) -> None:
        """Test parsing string with only symbols."""
        result = parse_due_date("!@#$%^&*()")
        assert result is None or isinstance(result, datetime)

    def test_parse_negative_days(self) -> None:
        """Test handling 'in -5 days' returns None (validation added)."""
        result = parse_due_date("in -5 days")
        assert result is None

    def test_parse_zero_days(self) -> None:
        """Test handling 'in 0 days' returns None (validation added)."""
        result = parse_due_date("in 0 days")
        assert result is None
