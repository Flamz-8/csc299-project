def format_date(date):
    """Format a date object into a string."""
    return date.strftime("%Y-%m-%d")

def validate_input(input_value, expected_type):
    """Validate the input value against the expected type."""
    if not isinstance(input_value, expected_type):
        raise ValueError(f"Expected input of type {expected_type}, got {type(input_value)}")

def calculate_time_remaining(start_time, duration):
    """Calculate the remaining time for a study session."""
    from datetime import datetime, timedelta
    end_time = start_time + timedelta(minutes=duration)
    return max(0, (end_time - datetime.now()).total_seconds())

def parse_task_input(task_input):
    """Parse a task input string into a dictionary."""
    parts = task_input.split('|')
    if len(parts) < 2:
        raise ValueError("Task input must be in the format 'title|description'")
    return {
        'title': parts[0].strip(),
        'description': parts[1].strip(),
        'due_date': parts[2].strip() if len(parts) > 2 else None
    }