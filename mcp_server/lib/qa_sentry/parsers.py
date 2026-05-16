"""
QA Sentry - JSON Parsers
Robust JSON sanitization and schema validation for LLM output
"""

import json
import re
from typing import Dict, Any


def sanitize_json(raw_response: str) -> str:
    """
    Robust JSON cleaning before parsing.

    Handles:
    - Markdown code blocks (```json ... ```)
    - Leading/trailing whitespace
    - Conversational prefixes
    - Multiple JSON objects (take first valid one)

    Args:
        raw_response: Raw LLM output

    Returns:
        Cleaned JSON string
    """
    # Strip markdown wrappers
    text = re.sub(r'^```json\s*', '', raw_response, flags=re.MULTILINE)
    text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)

    # Remove conversational prefixes (e.g., "Here's the analysis:")
    text = re.sub(r'^[^{]*(?={)', '', text, flags=re.DOTALL)

    # Strip trailing text after JSON
    # Find the last closing brace that matches the first opening brace
    brace_count = 0
    last_valid_pos = -1
    for i, char in enumerate(text):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                last_valid_pos = i + 1
                break

    if last_valid_pos > 0:
        text = text[:last_valid_pos]

    # Clean whitespace
    text = text.strip()

    return text


def validate_json_schema(data: Dict[str, Any]) -> bool:
    """
    Validate that JSON matches expected QA Sentry schema.

    Args:
        data: Parsed JSON data

    Returns:
        True if valid, False otherwise
    """
    try:
        # Check required top-level keys
        if 'summary' not in data or 'findings' not in data:
            return False

        # Check summary structure
        summary = data['summary']
        if not all(k in summary for k in ['health_score', 'risk_level', 'executive_summary']):
            return False

        # Check findings structure
        if not isinstance(data['findings'], list):
            return False

        for finding in data['findings']:
            required_keys = [
                'id', 'category', 'severity', 'line_numbers',
                'title', 'deep_dive', 'solution_explanation', 'reference', 'fix_code_snippet'
            ]
            if not all(k in finding for k in required_keys):
                return False

        return True
    except Exception:
        return False


# Fallback structure when LLM returns unparseable output
FALLBACK_RESULT = {
    "summary": {
        "health_score": 50,
        "risk_level": "MEDIUM",
        "executive_summary": "Analysis completed but output could not be fully parsed"
    },
    "findings": []
}
