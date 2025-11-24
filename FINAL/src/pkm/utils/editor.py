"""External editor integration for note editing.

Respects $EDITOR environment variable with platform-specific fallbacks.
"""

import os
import platform
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


def get_default_editor() -> str:
    """Get the default editor for the current platform.

    Returns:
        str: The name of the default text editor executable
    """
    system = platform.system()

    if system == "Windows":
        return "notepad.exe"
    elif system == "Darwin":  # macOS
        return "nano"
    else:  # Linux and others
        return "nano"


def open_in_editor(content: str, file_extension: str = ".txt") -> Optional[str]:
    """Open content in external editor and return the edited result.

    Args:
        content: Initial content to edit
        file_extension: File extension for the temporary file (default: .txt)

    Returns:
        str | None: Edited content, or None if editing was cancelled/failed

    Raises:
        RuntimeError: If the editor fails to launch or exits with error
    """
    # Get editor from environment or use platform default
    editor = os.environ.get("EDITOR", get_default_editor())

    # Create temporary file with initial content
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=file_extension,
        delete=False,
        encoding="utf-8"
    ) as tmp_file:
        tmp_file.write(content)
        tmp_path = Path(tmp_file.name)

    try:
        # Launch editor
        result = subprocess.run(
            [editor, str(tmp_path)],
            check=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Editor exited with code {result.returncode}")

        # Read edited content
        edited_content = tmp_path.read_text(encoding="utf-8")

        # Return None if content unchanged
        if edited_content == content:
            return None

        return edited_content

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to launch editor '{editor}': {e}")
    except FileNotFoundError:
        raise RuntimeError(
            f"Editor '{editor}' not found. Set EDITOR environment variable or install {get_default_editor()}"
        )
    finally:
        # Clean up temporary file
        try:
            tmp_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors
