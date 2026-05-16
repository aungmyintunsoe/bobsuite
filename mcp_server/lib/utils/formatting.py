"""
Formatting - Markdown header generation and timestamp utilities
"""

from datetime import datetime


def get_timestamp() -> str:
    """Get current timestamp in ISO format with Z suffix"""
    return datetime.utcnow().isoformat() + "Z"


def format_markdown_header(title: str, metadata: dict) -> str:
    """Format a standard markdown header for reports and docs"""
    lines = [f"# {title}"]
    for key, value in metadata.items():
        # Format key: capitalize and replace underscores with spaces
        display_key = key.replace('_', ' ').capitalize()
        lines.append(f"\n**{display_key}:** {value}")

    lines.append("\n\n---\n")
    return "".join(lines)
