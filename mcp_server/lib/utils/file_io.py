"""
File I/O - Safe file reading and language detection
"""

from pathlib import Path
from typing import Optional, Tuple
from lib.utils.constants import SUPPORTED_EXTENSIONS


def detect_language(file_path: str) -> str:
    """Detect programming language from file extension"""
    ext = Path(file_path).suffix.lower()
    return SUPPORTED_EXTENSIONS.get(ext, "Unknown")


def read_file_safe(file_path: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Safely read a file's content

    Returns:
        tuple: (content, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read(), None
    except FileNotFoundError:
        return None, f"File not found: {file_path}"
    except UnicodeDecodeError:
        return None, f"Unable to decode file as UTF-8: {file_path}"
    except Exception as e:
        return None, f"Error reading file: {str(e)}"
