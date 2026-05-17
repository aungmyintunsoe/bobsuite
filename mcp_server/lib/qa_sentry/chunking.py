"""
QA Sentry - Chunking Engine
Split large files into chunks and analyze concurrently with cross-file context support
"""

import asyncio
from typing import Dict, Any, List, Optional

from lib.utils import read_file_safe, get_timestamp
from lib.qa_sentry.agents import finder_pass


async def chunk_and_analyze(
    watsonx,
    code: str,
    file_path: str,
    language: str,
    system_prompt: str,
    chunk_size: int = 1000,
    temperature: float = 0.1,
    max_tokens: int = 4000,
    additional_context: Optional[str] = None
) -> Dict[str, Any]:
    """Split large files into chunks and analyze concurrently."""
    lines = code.split('\n')
    chunks = []

    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i + chunk_size]
        chunk_code = '\n'.join(chunk_lines)
        chunks.append({
            'code': chunk_code,
            'start_line': i + 1,
            'end_line': min(i + chunk_size, len(lines))
        })

    # Analyze chunks concurrently
    tasks = [
        _analyze_chunk(
            watsonx, chunk, file_path, language,
            system_prompt, temperature, max_tokens,
            additional_context
        )
        for chunk in chunks
    ]

    chunk_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Merge results
    all_findings = []
    total_health_score = 0
    valid_chunks = 0

    for result in chunk_results:
        if isinstance(result, dict) and 'findings' in result:
            all_findings.extend(result['findings'])
            total_health_score += result.get('summary', {}).get('health_score', 50)
            valid_chunks += 1

    avg_health_score = total_health_score // valid_chunks if valid_chunks > 0 else 50

    if avg_health_score < 30:
        risk_level = "CRITICAL"
    elif avg_health_score < 50:
        risk_level = "HIGH"
    elif avg_health_score < 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "success": True,
        "file_path": file_path,
        "language": language,
        "timestamp": get_timestamp(),
        "summary": {
            "health_score": avg_health_score,
            "risk_level": risk_level,
            "executive_summary": f"Large file analyzed in {len(chunks)} chunks with {len(all_findings)} total findings"
        },
        "findings": all_findings,
        "lines_analyzed": len(lines),
        "chunks_processed": len(chunks)
    }


async def _analyze_chunk(
    watsonx,
    chunk: Dict[str, Any],
    file_path: str,
    language: str,
    system_prompt: str,
    temperature: float = 0.1,
    max_tokens: int = 4000,
    additional_context: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze a single chunk of code."""
    try:
        finder_results = await finder_pass(
            watsonx,
            chunk['code'],
            language,
            f"{file_path} (lines {chunk['start_line']}-{chunk['end_line']})",
            system_prompt,
            temperature,
            max_tokens,
            additional_context
        )

        # Adjust line numbers to reflect actual file position
        for finding in finder_results.get('findings', []):
            finding['line_numbers'] = [
                ln + chunk['start_line'] - 1
                for ln in finding.get('line_numbers', [])
            ]

        return finder_results
    except Exception as e:
        return {
            "summary": {
                "health_score": 50,
                "risk_level": "MEDIUM",
                "executive_summary": f"Error analyzing chunk: {str(e)}"
            },
            "findings": []
        }


async def build_cross_file_context(file_paths: List[str]) -> str:
    """Extract interfaces/signatures from related files for context."""
    context_parts = []

    for path in file_paths:
        code, error = read_file_safe(path)
        if code:
            lines = code.split('\n')[:50]
            signatures = '\n'.join(lines)
            context_parts.append(f"# {path}\n{signatures}\n")

    return "\n".join(context_parts)
