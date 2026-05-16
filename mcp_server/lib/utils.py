"""
Utility functions and constants for BobSuite MCP
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# Supported programming languages and their extensions
SUPPORTED_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.h': 'C/C++ Header',
    '.hpp': 'C++ Header',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.cs': 'C#',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'Less',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.ini': 'INI',
    '.md': 'Markdown',
    '.txt': 'Text',
    '.rst': 'reStructuredText',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.sql': 'SQL',
}

def detect_language(file_path: str) -> str:
    """Detect programming language from file extension"""
    ext = Path(file_path).suffix.lower()
    return SUPPORTED_EXTENSIONS.get(ext, "Unknown")

def get_timestamp() -> str:
    """Get current timestamp in ISO format with Z suffix"""
    return datetime.utcnow().isoformat() + "Z"

def read_file_safe(file_path: str) -> tuple[Optional[str], Optional[str]]:
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

def format_markdown_header(title: str, metadata: dict) -> str:
    """Format a standard markdown header for reports and docs"""
    lines = [f"# {title}"]
    for key, value in metadata.items():
        # Format key: capitalize and replace underscores with spaces
        display_key = key.replace('_', ' ').capitalize()
        lines.append(f"\n**{display_key}:** {value}")
    
    lines.append("\n\n---\n")
    return "".join(lines)
