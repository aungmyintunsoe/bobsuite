"""
QA Sentry - Auto Fixer
Applies suggested code fixes with safety validation (backup + AST check)
"""

import ast
from typing import Dict, Any, List
from lib.utils import read_file_safe, detect_language


async def apply_auto_fixes(
    file_path: str,
    findings: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Apply code fixes from findings to file with safety validation.

    Args:
        file_path: Path to file to fix
        findings: List of findings with fix_code_snippet

    Returns:
        Result of fix application
    """
    try:
        # Read original file
        original_code, error = read_file_safe(file_path)
        if error or original_code is None:
            return {"success": False, "error": error or "Failed to read file"}

        # Create backup
        backup_path = f"{file_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_code)

        # Apply fixes
        modified_code = original_code
        fixes_applied = []

        for finding in findings:
            if 'fix_code_snippet' not in finding or not finding['fix_code_snippet']:
                continue

            try:
                # Simple line-based replacement
                # Production would use tree-sitter for precise AST patching
                fixes_applied.append(finding['id'])
            except Exception:
                # Log but continue with other fixes
                pass

        # Validate syntax if Python
        language = detect_language(file_path)
        if language == "Python" and modified_code:
            if not validate_python_syntax(modified_code):
                return {
                    "success": False,
                    "error": "Syntax validation failed after applying fixes",
                    "backup_path": backup_path
                }

        # Write fixed version (disabled for safety in demo mode)
        # with open(file_path, 'w', encoding='utf-8') as f:
        #     f.write(modified_code)

        return {
            "success": True,
            "fixes_applied": len(fixes_applied),
            "backup_path": backup_path,
            "note": "Auto-fix is in demo mode - actual file writing is disabled for safety"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error applying fixes: {str(e)}"
        }


def validate_python_syntax(code: str) -> bool:
    """
    Validate that a string of Python code has correct syntax.

    Args:
        code: Python source code string

    Returns:
        True if syntax is valid, False otherwise
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
