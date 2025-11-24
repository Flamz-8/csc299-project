"""Natural language date parsing utilities."""

from datetime import datetime, time
from typing import Optional

from dateutil.parser import parse as dateutil_parse
from dateutil.relativedelta import relativedelta


def parse_due_date(date_str: str) -> Optional[datetime]:
    """Parse a date string into a datetime object.

    Supports multiple formats:
    - Natural language: "tomorrow", "next Friday", "in 3 days"
    - ISO format: "2025-12-01"
    - Human format: "Dec 1", "December 1 2025"
    - With times: "Friday 11:59pm", "tomorrow at 5pm"

    Args:
        date_str: The date string to parse

    Returns:
        datetime object or None if parsing fails

    Examples:
        >>> parse_due_date("tomorrow")
        datetime(2025, 11, 24, 23, 59, 59)
        >>> parse_due_date("2025-12-01")
        datetime(2025, 12, 1, 23, 59, 59)
        >>> parse_due_date("Friday 11:59pm")
        datetime(2025, 11, 25, 23, 59, 0)
    """
    if not date_str or not date_str.strip():
        return None

    date_str = date_str.strip().lower()
    now = datetime.now()

    # Handle special cases first
    if date_str in ["today", "tonight"]:
        return datetime.combine(now.date(), time(23, 59, 59))

    if date_str == "tomorrow":
        tomorrow = now.date() + relativedelta(days=1)
        return datetime.combine(tomorrow, time(23, 59, 59))

    # Handle "next [day]" (e.g., "next friday")
    if date_str.startswith("next "):
        day_name = date_str[5:]
        try:
            # Parse the day name
            target = dateutil_parse(day_name, fuzzy=True)
            # Find the next occurrence of that day
            days_ahead = (target.weekday() - now.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7  # Next week, not today
            next_day = now.date() + relativedelta(days=days_ahead)
            return datetime.combine(next_day, time(23, 59, 59))
        except (ValueError, AttributeError):
            pass

    # Handle "in X days/weeks/months"
    if date_str.startswith("in "):
        parts = date_str[3:].split()
        if len(parts) >= 2:
            try:
                count = int(parts[0])
                unit = parts[1].rstrip('s')  # Remove plural 's'

                if unit in ["day", "days"]:
                    target_date = now.date() + relativedelta(days=count)
                elif unit in ["week", "weeks"]:
                    target_date = now.date() + relativedelta(weeks=count)
                elif unit in ["month", "months"]:
                    target_date = now.date() + relativedelta(months=count)
                else:
                    target_date = None

                if target_date:
                    return datetime.combine(target_date, time(23, 59, 59))
            except (ValueError, IndexError):
                pass

    # Try general parsing with dateutil
    try:
        parsed = dateutil_parse(date_str, fuzzy=True, default=now)

        # If only date was provided (no time), default to end of day
        if ":" not in date_str and "am" not in date_str and "pm" not in date_str:
            parsed = datetime.combine(parsed.date(), time(23, 59, 59))

        return parsed
    except (ValueError, AttributeError):
        return None


def format_due_date(dt: datetime) -> str:
    """Format a datetime into a human-readable due date string.

    Args:
        dt: The datetime to format

    Returns:
        Formatted string like "Friday, Nov 25 at 11:59 PM (2 days)"

    Examples:
        >>> dt = datetime(2025, 11, 25, 23, 59, 0)
        >>> format_due_date(dt)
        'Friday, Nov 25 at 11:59 PM (2 days)'
    """
    now = datetime.now()
    days_until = (dt.date() - now.date()).days

    # Format the date part
    date_str = dt.strftime("%A, %b %d")
    time_str = dt.strftime("at %I:%M %p").replace(" 0", " ")  # Remove leading zero from hour

    # Add relative time indicator
    if days_until == 0:
        relative = "today"
    elif days_until == 1:
        relative = "tomorrow"
    elif days_until == -1:
        relative = "yesterday"
    elif days_until < 0:
        relative = f"{abs(days_until)} days ago"
    else:
        relative = f"{days_until} days"

    return f"{date_str} {time_str} ({relative})"
