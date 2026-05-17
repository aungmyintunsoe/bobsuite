"""
QA Sentry - Reporting
Markdown report generation from scan results
"""

from typing import Dict, Any, List, Optional

from lib.utils import get_timestamp, format_markdown_header


def generate_report(
    scan_results: List[Dict[str, Any]],
    output_path: Optional[str] = None
) -> str:
    """Generate a markdown report from scan results."""
    # Ensure scan_results is a list
    if not isinstance(scan_results, list):
        scan_results = [scan_results] if scan_results else []
    
    report_lines = [
        format_markdown_header("Code Quality Analysis Report", {
            "generated": get_timestamp(),
            "total_files_scanned": len(scan_results)
        })
    ]

    for result in scan_results:
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            report_lines.append(f"\n## Invalid Result")
            report_lines.append(f"\n**Error:** Result is not a dictionary (type: {type(result).__name__})\n")
            continue
            
        if not result.get("success"):
            report_lines.append(f"\n## {result.get('file_path', 'Unknown')}")
            report_lines.append(f"\n**Error:** {result.get('error', 'Unknown error')}")
            if result.get('traceback'):
                report_lines.append(f"\n\n**Traceback:**\n```\n{result.get('traceback')}\n```")
            report_lines.append("\n")
            continue

        summary = result.get("summary", {})
        report_lines.append(f"\n## {result['file_path']}")
        report_lines.append(f"\n**Language:** {result.get('language', 'Unknown')}")
        report_lines.append(f"\n**Health Score:** {summary.get('health_score', 'N/A')}")
        report_lines.append(f"\n**Risk Level:** {summary.get('risk_level', 'N/A')}")
        report_lines.append(f"\n**Findings:** {len(result.get('findings', []))}")

        for finding in result.get('findings', []):
            report_lines.append(f"\n\n### [{finding.get('severity', '?')}] {finding.get('title', 'Untitled')}")
            report_lines.append(f"\n**Lines:** {finding.get('line_numbers', [])}")
            report_lines.append(f" | **ID:** {finding.get('id', '?')} | **Category:** {finding.get('category', '?')}")
            
            report_lines.append(f"\n\n#### The Problem")
            report_lines.append(f"\n> {finding.get('deep_dive', 'N/A')}")
            
            report_lines.append(f"\n\n#### The Solution")
            if finding.get('solution_explanation'):
                report_lines.append(f"\n{finding.get('solution_explanation')}")
            
            if finding.get('fix_code_snippet'):
                report_lines.append(f"\n\n```python\n{finding['fix_code_snippet']}\n```")
            
            report_lines.append(f"\n\n**Reference:** {finding.get('reference', 'N/A')}")

        report_lines.append("\n\n---\n")

    report = "\n".join(report_lines)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

    return report
