"""
QA Sentry Prompts - Centralized prompt templates for code quality analysis
Extracted for better maintainability and versioning
"""

from typing import Dict, Any, Optional
import json


def build_finder_prompt(
    code: str,
    language: str,
    file_path: str,
    system_context: str,
    additional_context: Optional[str] = None
) -> str:
    """
    Build the Finder pass prompt for aggressive issue detection.
    
    Args:
        code: Source code to analyze
        language: Programming language
        file_path: Path to the file being analyzed
        system_context: System prompt with schema and examples
        additional_context: Optional cross-file context
    
    Returns:
        Formatted prompt string
    """
    context_section = f"\n\nADDITIONAL CONTEXT:\n{additional_context}" if additional_context else ""
    
    prompt = f"""{system_context}

LANGUAGE: {language}
FILE: {file_path}{context_section}

CODE TO ANALYZE:
```{language}
{code}
```

OUTPUT: Return ONLY valid JSON matching the schema above. No markdown, no explanations.
"""
    
    return prompt


def build_critic_prompt(
    code: str,
    finder_results: Dict[str, Any],
    language: str,
    file_path: str
) -> str:
    """
    Build the Critic pass prompt for verification and false positive removal.
    
    Args:
        code: Original source code
        finder_results: Results from the Finder pass
        language: Programming language
        file_path: Path to the file being analyzed
    
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are a Senior Staff Engineer conducting a final corporate code audit.

LANGUAGE: {language}
FILE: {file_path}

ORIGINAL CODE:
```{language}
{code}
```

INITIAL FINDINGS FROM AUTOMATED SCAN:
{json.dumps(finder_results, indent=2)}

YOUR TASK:
1. Review each finding for false positives
2. Remove any issues that are:
   - Style/formatting (assume linter handles this)
   - Subjective preferences
   - Not 95%+ confident bugs
3. Recalculate health_score based on remaining issues
4. Keep only HIGH-CONFIDENCE findings

Return ONLY valid JSON matching this schema:
{{
  "summary": {{"health_score": 0-100, "risk_level": "CRITICAL|HIGH|MEDIUM|LOW", "executive_summary": "string"}},
  "findings": [{{"id": "string", "category": "string", "severity": "string", "line_numbers": [], "title": "string", "deep_dive": "string", "solution_explanation": "string", "reference": "string", "fix_code_snippet": "string"}}]
}}

OUTPUT: Valid JSON only, no markdown, no explanations.
"""
    
    return prompt


# Made with Bob