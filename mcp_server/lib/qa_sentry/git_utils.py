"""
QA Sentry - Git Utilities
Git diff scanning and hunk parsing for targeted code analysis
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, Any, List


async def scan_git_diff(
    sentry,
    repo_path: str,
    staged: bool = True
) -> List[Dict[str, Any]]:
    """
    Scan only changed lines from git diff.

    Args:
        sentry: QASentry instance (for calling scan_code)
        repo_path: Path to git repository
        staged: If True, scan staged changes; else scan working directory

    Returns:
        List of findings for changed lines only
    """
    try:
        # Get diff
        cmd = ['git', 'diff', '--staged'] if staged else ['git', 'diff', 'HEAD']
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return [{
                "success": False,
                "error": f"Git command failed: {result.stderr}"
            }]

        # Parse diff hunks
        changed_files = parse_diff_hunks(result.stdout)

        if not changed_files:
            return [{
                "success": True,
                "message": "No changes detected in git diff"
            }]

        # Analyze each changed file
        all_results = []
        for file_info in changed_files:
            full_path = Path(repo_path) / file_info['path']
            if not full_path.exists():
                continue

            # Scan the file using sentry's core pipeline
            scan_result = await sentry.scan_code(str(full_path))

            if scan_result.get('success'):
                # Filter findings to only changed lines
                filtered_findings = [
                    f for f in scan_result.get('findings', [])
                    if any(ln in file_info['changed_lines'] for ln in f.get('line_numbers', []))
                ]
                scan_result['findings'] = filtered_findings
                scan_result['git_diff_filtered'] = True
                scan_result['changed_lines'] = file_info['changed_lines']

            all_results.append(scan_result)

        return all_results

    except subprocess.TimeoutExpired:
        return [{
            "success": False,
            "error": "Git command timed out"
        }]
    except Exception as e:
        return [{
            "success": False,
            "error": f"Error scanning git diff: {str(e)}",
            "error_type": type(e).__name__
        }]


def parse_diff_hunks(diff_output: str) -> List[Dict[str, Any]]:
    """
    Parse git diff output to extract changed line numbers.

    Format: @@ -old_start,old_count +new_start,new_count @@

    Args:
        diff_output: Raw git diff output

    Returns:
        List of file info with changed lines
    """
    files = []
    current_file = None

    for line in diff_output.split('\n'):
        # File header
        if line.startswith('+++'):
            path = line[6:]  # Remove '+++ b/'
            if path and path != '/dev/null':
                current_file = {'path': path, 'changed_lines': []}
                files.append(current_file)

        # Hunk header
        elif line.startswith('@@') and current_file:
            match = re.search(r'\+(\d+),(\d+)', line)
            if match:
                start = int(match.group(1))
                count = int(match.group(2))
                current_file['changed_lines'].extend(range(start, start + count))

    return files
