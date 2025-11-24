"""ID generator service."""

from pkm.models.common import generate_id as _generate_id


def generate_note_id() -> str:
    """Generate a unique note ID.

    Returns:
        Note ID in format: n_YYYYMMDD_HHMMSS_xxx
    """
    return _generate_id("n")


def generate_task_id() -> str:
    """Generate a unique task ID.

    Returns:
        Task ID in format: t_YYYYMMDD_HHMMSS_xxx
    """
    return _generate_id("t")


def generate_course_id() -> str:
    """Generate a unique course ID.

    Returns:
        Course ID in format: c_YYYYMMDD_HHMMSS_xxx
    """
    return _generate_id("c")
