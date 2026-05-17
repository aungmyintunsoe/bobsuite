"""
QA Sentry - Agent Passes
Multi-Agent AI debate pattern: Finder (aggressive detection) → Critic (verification)
"""

import json
from typing import Dict, Any, Optional

from lib.qa_sentry.parsers import sanitize_json, validate_json_schema
from lib.qa_sentry.prompts import build_finder_prompt, build_critic_prompt


async def finder_pass(
    watsonx,
    code: str,
    language: str,
    file_path: str,
    system_prompt: str,
    temperature: float = 0.1,
    max_tokens: int = 4000,
    additional_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Pass 1: The Finder - Aggressive issue detection.

    Returns raw JSON with all potential issues.
    """
    prompt = build_finder_prompt(
        code=code,
        language=language,
        file_path=file_path,
        system_context=system_prompt,
        additional_context=additional_context
    )

    try:
        response = await watsonx.generate_text(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

        clean_json = sanitize_json(response)
        data = json.loads(clean_json)

        if not validate_json_schema(data):
            raise ValueError("Response does not match expected schema")

        return data
    except json.JSONDecodeError as e:
        return {
            "summary": {
                "health_score": 50,
                "risk_level": "MEDIUM",
                "executive_summary": f"JSON parsing error in Finder pass: {str(e)}"
            },
            "findings": []
        }
    except Exception as e:
        return {
            "summary": {
                "health_score": 50,
                "risk_level": "MEDIUM",
                "executive_summary": f"Error in Finder pass: {str(e)}"
            },
            "findings": []
        }


async def critic_pass(
    watsonx,
    code: str,
    finder_results: Dict[str, Any],
    language: str,
    file_path: str,
    temperature: float = 0.1,
    max_tokens: int = 4000
) -> Dict[str, Any]:
    """
    Pass 2: The Critic - Verification and pruning of false positives.

    Returns hardened, verified JSON.
    """
    prompt = build_critic_prompt(
        code=code,
        finder_results=finder_results,
        language=language,
        file_path=file_path
    )

    try:
        response = await watsonx.generate_text(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

        clean_json = sanitize_json(response)
        data = json.loads(clean_json)

        if not validate_json_schema(data):
            # If Critic fails validation, return Finder results
            return finder_results

        return data
    except Exception:
        # If Critic fails, return Finder results
        return finder_results
