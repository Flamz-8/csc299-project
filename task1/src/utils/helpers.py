def format_date(date):
    # Format the date to a more readable format
    return date.strftime("%Y-%m-%d")

def parse_date(date_string):
    # Parse a date string into a date object
    from datetime import datetime
    return datetime.strptime(date_string, "%Y-%m-%d")

def validate_task_title(title):
    # Validate that the task title is not empty
    if not title or len(title.strip()) == 0:
        raise ValueError("Task title cannot be empty.")

def validate_event_details(event):
    # Validate event details
    if 'title' not in event or 'date' not in event:
        raise ValueError("Event must have a title and a date.")
    validate_task_title(event['title'])