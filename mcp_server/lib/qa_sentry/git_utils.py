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
    staged: bool = True,
    max_files: int = 10,
    max_file_size_kb: int = 500
) -> List[Dict[str, Any]]:
    """
    Scan only changed lines from git diff with limits to prevent timeouts.

    Args:
        sentry: QASentry instance (for calling scan_code)
        repo_path: Path to git repository
        staged: If True, scan staged changes; else scan working directory
        max_files: Maximum number of files to scan (default: 10)
        max_file_size_kb: Maximum file size in KB to scan (default: 500KB)

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

        # Apply file count limit
        if len(changed_files) > max_files:
            return [{
                "success": False,
                "error": f"Too many changed files ({len(changed_files)}). Maximum allowed: {max_files}",
                "suggestion": "Commit changes in smaller batches or increase max_files parameter",
                "changed_file_count": len(changed_files),
                "max_files": max_files
            }]

        # Analyze each changed file with size checks
        all_results = []
        skipped_files = []
        
        for file_info in changed_files:
            full_path = Path(repo_path) / file_info['path']
            
            if not full_path.exists():
                continue

            # Check file size
            file_size_kb = full_path.stat().st_size / 1024
            if file_size_kb > max_file_size_kb:
                skipped_files.append({
                    "path": file_info['path'],
                    "size_kb": round(file_size_kb, 2),
                    "reason": f"File too large ({round(file_size_kb, 2)}KB > {max_file_size_kb}KB)"
                })
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

        # Add summary if files were skipped
        if skipped_files:
            all_results.insert(0, {
                "success": True,
                "message": f"Scanned {len(all_results)} files, skipped {len(skipped_files)} files",
                "skipped_files": skipped_files
            })

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
