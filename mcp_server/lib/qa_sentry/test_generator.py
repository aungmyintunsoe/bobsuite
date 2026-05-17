"""
QA Sentry - Test Generator
Dynamic test generation that adapts to user needs.
Loads the SDET Vanguard persona from test_persona.txt and composes
prompts dynamically based on the requested test type.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from lib.utils import detect_language, get_timestamp, read_file_safe
from lib.qa_sentry.parsers import sanitize_json
from lib.qa_sentry.prompts import (
    build_network_performance_test_prompt,
    build_unit_test_generation_prompt
)


def load_testing_persona() -> str:
    """
    Load the SDET Vanguard testing persona from test_persona.txt.
    This provides the foundational testing principles and autonomous
    execution protocols for all test generation.
    """
    try:
        persona_path = Path(__file__).parent / "test_persona.txt"
        with open(persona_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        # Fallback persona if file is missing
        return """You are "SDET Vanguard Bob" — an elite Software Development Engineer in Test.
You autonomously build testing environments, manage dependencies, execute test suites,
and write high-fidelity tests that perfectly specify component behavior.
Follow Steve Sanderson Unit Testing Principles with S/S/R naming convention."""


async def generate_tests(
    watsonx,
    file_path: str,
    test_type: str = "unit",
    testing_library: Optional[str] = None,
    test_requirements: Optional[str] = None
) -> Dict[str, Any]:
    """
    Dynamically generate tests based on user needs.

    This is the unified entry point that adapts the test generation
    strategy based on what the user actually wants — unit tests,
    network/performance tests, integration tests, etc.

    Args:
        watsonx: WatsonxClient instance
        file_path: Path to the code file to generate tests for
        test_type: Type of tests to generate ('unit', 'network', 'integration', 'e2e', 'api')
        testing_library: Optional specific testing library
        test_requirements: Optional specific requirements for the tests

    Returns:
        Dictionary containing test files, setup commands, and execution instructions
    """
    try:
        # Read the file
        code, error = read_file_safe(file_path)
        if error or code is None:
            return {
                "success": False,
                "error": error or "Failed to read file",
                "file_path": file_path
            }

        # Detect language
        language = detect_language(file_path)
        if not language or language == "Unknown":
            language = "text"

        # Load the SDET Vanguard persona from test_persona.txt
        testing_persona = load_testing_persona()

        # Build the appropriate prompt based on test type
        prompt = _build_dynamic_prompt(
            code=code,
            language=language,
            file_path=file_path,
            test_type=test_type,
            testing_persona=testing_persona,
            testing_library=testing_library,
            test_requirements=test_requirements
        )

        # Generate tests using watsonx
        response = await watsonx.generate_text(
            prompt,
            temperature=0.2,  # Slightly higher for creative test generation
            max_tokens=6000   # More tokens for comprehensive test suites
        )

        # Parse the JSON response
        clean_json = sanitize_json(response)
        test_data = json.loads(clean_json)

        # Build result with common fields
        result = {
            "success": True,
            "file_path": file_path,
            "language": language,
            "timestamp": get_timestamp(),
            "test_type": test_type,
            "test_framework": test_data.get("test_framework"),
            "framework_justification": test_data.get("framework_justification"),
            "dependencies": test_data.get("dependencies", []),
            "setup_commands": test_data.get("setup_commands", []),
            "test_files": test_data.get("test_files", []),
            "execution_command": test_data.get("execution_command"),
            "configuration_files": test_data.get("configuration_files", []),
            "notes": test_data.get("notes", "")
        }

        # Add type-specific fields
        if test_type == "network":
            result["performance_thresholds"] = test_data.get("performance_thresholds", {})
            result["test_scenarios"] = test_data.get("test_scenarios", [])
        else:
            # Unit / integration / e2e tests get mock + coverage info
            result["mock_strategy"] = test_data.get("mock_strategy", {})
            result["test_coverage"] = test_data.get("test_coverage", {})
            result["design_principles_applied"] = test_data.get("design_principles_applied", [])

        return result

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON parsing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": type(e).__name__,
            "file_path": file_path
        }


def _build_dynamic_prompt(
    code: str,
    language: str,
    file_path: str,
    test_type: str,
    testing_persona: str,
    testing_library: Optional[str] = None,
    test_requirements: Optional[str] = None
) -> str:
    """
    Dynamically compose a test generation prompt based on the test type.

    Uses test_persona.txt as the foundational persona, then layers on
    type-specific instructions. This replaces the rigid, duplicated
    prompts that were hardcoded per test type.
    """
    # Route to existing specialized builders for backward compatibility
    if test_type == "network":
        return build_network_performance_test_prompt(
            code=code,
            language=language,
            file_path=file_path,
            testing_library=testing_library,
            test_requirements=test_requirements,
            testing_persona=testing_persona
        )
    elif test_type == "unit":
        return build_unit_test_generation_prompt(
            code=code,
            language=language,
            file_path=file_path,
            testing_library=testing_library,
            test_requirements=test_requirements,
            testing_persona=testing_persona
        )
    else:
        # Dynamic prompt for any other test type (integration, e2e, api, etc.)
        return _build_generic_test_prompt(
            code=code,
            language=language,
            file_path=file_path,
            test_type=test_type,
            testing_persona=testing_persona,
            testing_library=testing_library,
            test_requirements=test_requirements
        )


def _build_generic_test_prompt(
    code: str,
    language: str,
    file_path: str,
    test_type: str,
    testing_persona: str,
    testing_library: Optional[str] = None,
    test_requirements: Optional[str] = None
) -> str:
    """
    Build a generic test prompt for test types beyond unit/network.
    Uses the test_persona.txt persona as the foundation.
    """
    library_guidance = ""
    if testing_library:
        library_guidance = f"\n\nUSER REQUESTED TESTING LIBRARY: {testing_library}\nYou MUST use this library for the tests."
    else:
        library_guidance = f"\n\nAUTONOMOUS MODE: Select the most appropriate {test_type} testing library for this language and use case."

    requirements_section = ""
    if test_requirements:
        requirements_section = f"\n\nSPECIFIC TEST REQUIREMENTS:\n{test_requirements}"

    test_type_upper = test_type.upper().replace("_", " ")

    prompt = f"""{testing_persona}

# YOUR TASK: {test_type_upper} TEST GENERATION
Analyze the following code and create comprehensive {test_type} tests.

LANGUAGE: {language}
FILE: {file_path}{library_guidance}{requirements_section}

CODE TO ANALYZE:
```{language}
{code}
```

# OUTPUT REQUIREMENTS
You must output a JSON object with this exact schema:
{{
  "test_framework": "string (name of testing framework selected)",
  "framework_justification": "string (why this framework is optimal)",
  "dependencies": ["array of dependency install commands"],
  "setup_commands": ["array of setup/initialization commands"],
  "test_files": [
    {{
      "filename": "string",
      "content": "string (complete test file content)",
      "description": "string (what this test file covers)"
    }}
  ],
  "execution_command": "string (command to run the tests)",
  "configuration_files": [
    {{
      "filename": "string",
      "content": "string (complete config file content)",
      "description": "string (purpose of this config)"
    }}
  ],
  "mock_strategy": {{
    "external_dependencies": ["list of dependencies that will be mocked"],
    "mocking_library": "string",
    "mock_examples": ["array of key mocking patterns used"]
  }},
  "test_coverage": {{
    "units_tested": ["array of functions/classes/methods tested"],
    "test_count": "number",
    "coverage_notes": "string"
  }},
  "design_principles_applied": ["array of testing principles demonstrated"],
  "notes": "string (additional notes about test design decisions)"
}}

OUTPUT: Return ONLY valid JSON matching the schema above. No markdown, no explanations outside the JSON.
"""
    return prompt
