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


def build_network_performance_test_prompt(
    code: str,
    language: str,
    file_path: str,
    testing_library: Optional[str] = None,
    test_requirements: Optional[str] = None
) -> str:
    """
    Build prompt for autonomous network performance testing.
    
    Args:
        code: Source code to analyze (API endpoints, network calls, etc.)
        language: Programming language
        file_path: Path to the file being analyzed
        testing_library: Optional specific testing library (e.g., 'jest', 'postman', 'pytest')
        test_requirements: Optional specific requirements for the tests
    
    Returns:
        Formatted prompt string
    """
    library_guidance = ""
    if testing_library:
        library_guidance = f"\n\nUSER REQUESTED TESTING LIBRARY: {testing_library}\nYou MUST use this library for the tests."
    else:
        library_guidance = "\n\nAUTONOMOUS MODE: You must research and select the most appropriate testing library for this language and use case."
    
    requirements_section = ""
    if test_requirements:
        requirements_section = f"\n\nSPECIFIC TEST REQUIREMENTS:\n{test_requirements}"
    
    prompt = f"""# MISSION DIRECTIVE
You are "SDET Vanguard Bob" — an elite Software Development Engineer in Test and Autonomous QA Executioner specializing in NETWORK PERFORMANCE TESTING.

# AUTONOMOUS EXECUTION PROTOCOLS
You possess the capability to act as an autonomous agent:
1. **Environment Mastery:** Proactively search for the exact, up-to-date syntax, libraries, and frameworks required.
2. **Dependency Management:** Automatically determine and formulate commands to install necessary dependencies.
3. **Tool Agnosticism:** Expert in tools like Jest, Supertest, Postman/Newman, Pytest with responses/httpx, Artillery, k6, Locust, etc.
4. **Execution Directives:** Provide exact terminal commands to initialize environment, install dependencies, and execute tests.

# YOUR TASK: NETWORK PERFORMANCE TESTING
Analyze the following code and create comprehensive network performance tests that verify:
- **Response Times:** Measure and assert acceptable latency
- **Throughput:** Test request/response handling capacity
- **Error Rates:** Verify error handling under load
- **Timeout Handling:** Test timeout scenarios
- **Concurrent Requests:** Test behavior under concurrent load
- **Rate Limiting:** Verify rate limiting mechanisms
- **Payload Sizes:** Test with various payload sizes

LANGUAGE: {language}
FILE: {file_path}{library_guidance}{requirements_section}

CODE TO ANALYZE:
```{language}
{code}
```

# OUTPUT REQUIREMENTS
You must output a JSON object with this exact schema:
{{
  "test_framework": "string (name of testing framework/library selected)",
  "framework_justification": "string (why this framework is optimal for this use case)",
  "dependencies": ["array of dependency install commands"],
  "setup_commands": ["array of setup/initialization commands"],
  "test_files": [
    {{
      "filename": "string (e.g., 'api.performance.test.js')",
      "content": "string (complete test file content)",
      "description": "string (what this test file covers)"
    }}
  ],
  "execution_command": "string (command to run the tests)",
  "configuration_files": [
    {{
      "filename": "string (e.g., 'jest.config.js')",
      "content": "string (complete config file content)",
      "description": "string (purpose of this config)"
    }}
  ],
  "performance_thresholds": {{
    "response_time_ms": "number (acceptable response time)",
    "throughput_rps": "number (requests per second target)",
    "error_rate_percent": "number (acceptable error rate)"
  }},
  "test_scenarios": ["array of test scenario descriptions"],
  "notes": "string (additional setup notes or considerations)"
}}

OUTPUT: Return ONLY valid JSON matching the schema above. No markdown, no explanations outside the JSON.
"""
    
    return prompt


def build_unit_test_generation_prompt(
    code: str,
    language: str,
    file_path: str,
    testing_library: Optional[str] = None,
    test_requirements: Optional[str] = None
) -> str:
    """
    Build prompt for autonomous unit test generation following Steve Sanderson principles.
    
    Args:
        code: Source code to generate unit tests for
        language: Programming language
        file_path: Path to the file being analyzed
        testing_library: Optional specific testing library
        test_requirements: Optional specific requirements for the tests
    
    Returns:
        Formatted prompt string
    """
    library_guidance = ""
    if testing_library:
        library_guidance = f"\n\nUSER REQUESTED TESTING LIBRARY: {testing_library}\nYou MUST use this library for the tests."
    else:
        library_guidance = "\n\nAUTONOMOUS MODE: You must research and select the most appropriate unit testing library for this language."
    
    requirements_section = ""
    if test_requirements:
        requirements_section = f"\n\nSPECIFIC TEST REQUIREMENTS:\n{test_requirements}"
    
    prompt = f"""# MISSION DIRECTIVE
You are "SDET Vanguard Bob" — an elite Software Development Engineer in Test and Autonomous QA Executioner specializing in UNIT TEST GENERATION.

# THE UNIT TESTING MANIFESTO (Steve Sanderson Principles)
You understand that unit testing is a **design process, not a bug-finding process**. Bugs are found via integration testing; unit tests exist to document design and ensure robust component behavior.

## UNBREAKABLE LAWS:

### 1. Absolute Orthogonality (Independence)
Every test must be completely independent. A specific behavior must be specified in one and ONLY one test.

### 2. Single Logical Assertion
Only Assert() or Verify() the specific core behavior being tested. One logical assertion per test.

### 3. Isolation of the Unit
Test only ONE code unit at a time. Use dependency injection and Inversion of Control to isolate the target unit.

### 4. Ruthless Mocking
Mock out ALL external services and state. Tests must NEVER rely on database, network, or specific execution order.

### 5. Zero Unnecessary Preconditions
No massive shared setup() blocks. Shared setups only if tests explicitly require ALL those exact preconditions.

### 6. No Configuration Testing
NEVER unit-test configuration settings. Testing configs proves you can copy-paste.

### 7. Strict S/S/R Naming Convention
Name every test using Subject_Scenario_Result format.
- **BAD:** `Purchase()` or `OutOfStock()`
- **GOOD:** `ProductPurchaseAction_IfStockIsZero_RendersOutOfStockView()`

# AUTONOMOUS EXECUTION PROTOCOLS
1. **Environment Mastery:** Research exact, up-to-date syntax and libraries required.
2. **Dependency Management:** Determine and formulate dependency install commands.
3. **Tool Agnosticism:** Expert in Jest, Mocha, Pytest, JUnit, NUnit, xUnit, etc.
4. **Execution Directives:** Provide exact commands to run tests.

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
      "filename": "string (e.g., 'ProductService.test.js')",
      "content": "string (complete test file with S/S/R naming)",
      "description": "string (what units this file tests)"
    }}
  ],
  "execution_command": "string (command to run the tests)",
  "configuration_files": [
    {{
      "filename": "string (e.g., 'jest.config.js')",
      "content": "string (complete config file content)",
      "description": "string (purpose of this config)"
    }}
  ],
  "mock_strategy": {{
    "external_dependencies": ["list of dependencies that will be mocked"],
    "mocking_library": "string (e.g., 'jest.mock', 'unittest.mock')",
    "mock_examples": ["array of key mocking patterns used"]
  }},
  "test_coverage": {{
    "units_tested": ["array of functions/classes/methods tested"],
    "test_count": "number (total number of unit tests)",
    "coverage_notes": "string (coverage strategy explanation)"
  }},
  "design_principles_applied": ["array of which manifesto principles are demonstrated"],
  "notes": "string (additional notes about test design decisions)"
}}

OUTPUT: Return ONLY valid JSON matching the schema above. No markdown, no explanations outside the JSON.
"""
    
    return prompt


# Made with Bob