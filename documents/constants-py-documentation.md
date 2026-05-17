# Comprehensive Documentation for constants.py
**File:** mcp_server/lib/utils/constants.py
**Language:** Python
**Documentation type:** Comprehensive Documentation
**Generated:** 2026-05-17T09:35:53.115887Z

---

## API Documentation

### Application Constants

Centralized configuration values to eliminate magic numbers throughout the codebase.

### HTTP & NETWORK CONFIGURATION

- **HTTP_TIMEOUT_SECONDS** (float): HTTP timeout in seconds for API requests - `60.0`
- **MAX_RETRY_ATTEMPTS** (int): Maximum number of retry attempts for transient failures - `3`
- **RETRY_BASE_DELAY_SECONDS** (float): Base delay for exponential backoff (in seconds) - `1.0`

### TOKEN & AUTHENTICATION

- **TOKEN_EXPIRY_BUFFER_SECONDS** (int): Token expiration buffer in seconds (refresh 60s before actual expiry) - `60`
- **DEFAULT_TOKEN_EXPIRY_SECONDS** (int): Default token expiration time if not provided by API (in seconds) - `3600`

### AI MODEL PARAMETERS

- **DEFAULT_MAX_TOKENS** (int): Default maximum tokens for text generation - `2000`
- **PRD_MAX_TOKENS** (int): Maximum tokens for PRD synthesis (longer documents) - `4000`
- **DEFAULT_TEMPERATURE** (float): Default temperature for balanced creativity/structure - `0.7`
- **PRD_TEMPERATURE** (float): Temperature for PRD synthesis (more structured) - `0.4`
- **CODE_ANALYSIS_TEMPERATURE** (float): Temperature for code analysis (more deterministic) - `0.1`

### CODE ANALYSIS & CHUNKING

- **MAX_CHUNK_SIZE_LINES** (int): Maximum lines per code chunk for analysis - `1000`
- **MIN_CHUNK_SIZE_LINES** (int): Minimum lines to consider for chunking - `100`
- **CHUNK_OVERLAP_LINES** (int): Overlap between chunks (in lines) - `50`

### CACHE CONFIGURATION

- **DEFAULT_CACHE_TTL_SECONDS** (int): Default cache TTL in seconds (1 hour) - `3600`
- **CACHE_PATH_HASH_LENGTH** (int): Cache key path hash length (characters) - `8`

### FILE PROCESSING

- **MAX_FILE_SIZE_BYTES** (int): Maximum file size for processing (in bytes) - 10MB - `10 * 1024 * 1024`
- **DEFAULT_FILE_ENCODING** (str): Default encoding for file operations - `'utf-8'`
- **SUPPORTED_EXTENSIONS** (dict): Supported file extensions for code analysis (maps extension to language name)

### VISUALIZATION

- **DEFAULT_DEPENDENCY_MAX_DEPTH** (int): Default maximum depth for dependency analysis - `3`
- **KROKI_API_BASE_URL** (str): Kroki API base URL for diagram generation - `"https://kroki.io"`
- **MERMAID_COMPRESSION_LEVEL** (int): Compression level for Mermaid diagrams (1-9, 9 is maximum) - `9`

### QA SENTRY

- **SEVERITY_CRITICAL** (str): Severity level for critical code issues - `"critical"`
- **SEVERITY_HIGH** (str): Severity level for high code issues - `"high"`
- **SEVERITY_MEDIUM** (str): Severity level for medium code issues - `"medium"`
- **SEVERITY_LOW** (str): Severity level for low code issues - `"low"`
- **SCAN_TYPE_ALL** (str): Scan type to scan for all issues - `"all"`
- **SCAN_TYPE_SECURITY** (str): Scan type to scan for security issues - `"security"`
- **SCAN_TYPE_PERFORMANCE** (str): Scan type to scan for performance issues - `"performance"`
- **SCAN_TYPE_STYLE** (str): Scan type to scan for style issues - `"style"`

### HTTP STATUS CODES (for retry logic)

- **HTTP_STATUS_SERVER_ERROR_MIN** (int): Minimum value for server error status codes (retryable) - `500`
- **HTTP_STATUS_SERVER_ERROR_MAX** (int): Maximum value for server error status codes (retryable) - `599`
- **HTTP_STATUS_RATE_LIMIT** (int): Status code for rate limit (retryable) - `429`
- **HTTP_STATUS_OK** (int): Status code for successful requests - `200`

### Usage Examples

```python
import application_constants

# HTTP request with timeout
response = requests.get('https://api.example.com/data', 
                       timeout=application_constants.HTTP_TIMEOUT_SECONDS)

# Retry logic for transient failures
for attempt in range(application_constants.MAX_RETRY_ATTEMPTS):
    try:
        # Perform some operation
        break
    except TransientError:
        if attempt < application_constants.MAX_RETRY_ATTEMPTS - 1:
            time.sleep(application_constants.RETRY_BASE_DELAY_SECONDS * (2 ** attempt))
        else:
            raise

# Check file size before processing
if os.path.getsize(file_path) <= application_constants.MAX_FILE_SIZE_BYTES:
    process_file(file_path)
else:
    raise ValueError("File size exceeds the maximum allowed limit.")
```

## Quick Start Guide

### Minimal setup steps
1. Ensure you have Python 3.7 or higher installed.
2. Install the required dependencies mentioned in the project's requirements.txt file.
3. Import the constants module in your Python scripts: `from application_constants import *`.

### Basic usage example
```python
from application_constants import DEFAULT_MAX_TOKENS, PRD_TEMPERATURE

print(f"Default max tokens: {DEFAULT_MAX_TOKENS}")
print(f"PRD temperature: {PRD_TEMPERATURE}")
```

### Next steps
1. Review the constants and adjust their values according to your project's requirements.
2. Use the constants throughout your codebase to eliminate magic numbers.
3. If you need to add more constants, follow the existing structure and naming conventions.

### Links to detailed documentation
- Python documentation: https://docs.python.org/
- PEP 8 - Style Guide for Python Code: https://peps.python.org/pep-0008/

## User Manual

### Overview and Purpose
The provided code defines a set of application constants for a Python project. These constants centralize configuration values throughout the codebase, eliminating the use of "magic numbers" and making the code more maintainable and readable.

### Installation Instructions
1. Ensure that you have Python installed on your system.
2. Save the provided code in a file named `constants.py` in your project's directory.
3. Import the constants in your Python files:
   ```python
   from constants import HTTP_TIMEOUT_SECONDS, DEFAULT_TEMPERATURE, MAX_FILE_SIZE_BYTES
   ```

### Configuration Options
The code provides a wide range of configuration options that can be modified based on your application's requirements:

- **HTTP_TIMEOUT_SECONDS**: Set the timeout value in seconds for API requests.
- **MAX_RETRY_ATTEMPTS**: Specify the maximum number of retry attempts for transient failures.
- **TOKEN_EXPIRY_BUFFER_SECONDS**: Define the token expiration buffer in seconds.
- **DEFAULT_MAX_TOKENS**: Set the default maximum tokens for text generation.
- **MAX_CHUNK_SIZE_LINES**: Specify the maximum lines per code chunk for analysis.
- **DEFAULT_CACHE_TTL_SECONDS**: Set the default cache time-to-live (TTL) in seconds.
- **MAX_FILE_SIZE_BYTES**: Define the maximum file size for processing in bytes.

### Usage Examples

```python
from constants import HTTP_TIMEOUT_SECONDS, DEFAULT_TEMPERATURE, MAX_FILE_SIZE_BYTES

# Example 1: Making an API request with the configured timeout
response = requests.get("https://api.example.com/data", timeout=HTTP_TIMEOUT_SECONDS)

# Example 2: Generating text with the default temperature
text = generate_text(prompt, temperature=DEFAULT_TEMPERATURE)

# Example 3: Processing a file with the maximum file size limit
if os.path.getsize(file_path) <= MAX_FILE_SIZE_BYTES:
    process_file(file_path)
else:
    print("File exceeds the maximum size limit.")
```

### Common Use Cases
- Configuring HTTP requests with appropriate timeout values and retry attempts.
- Setting default values for AI model parameters like temperature and maximum tokens.
- Defining limits and thresholds for code analysis and chunking.
- Configuring cache settings like TTL and path hash length.
- Specifying file processing limits and supported file extensions.

### Best Practices
- Import only the constants that you need to avoid unnecessary dependencies.
- Use the constants consistently throughout your codebase.
- Document the purpose and usage of each constant.
- Consider grouping related constants into separate sections.
- Regularly review and update the constant values based on changes in requirements.
- Avoid hardcoding values directly in your code.
- Use meaningful and descriptive names for the constants.

## How-To Guide

### Objective
Define a set of application constants for centralized configuration values to eliminate magic numbers throughout the codebase.

### Prerequisites
- Python 3.x installed on your system.
- Basic understanding of Python programming language.

### Step-by-Step Instructions

1. Create a new Python file (e.g., `constants.py`) or open an existing file.

2. Add a docstring at the top to describe the purpose of the constants.

3. Define the HTTP & Network Configuration constants:
   - `HTTP_TIMEOUT_SECONDS`, `MAX_RETRY_ATTEMPTS`, `RETRY_BASE_DELAY_SECONDS`

4. Define the Token & Authentication constants:
   - `TOKEN_EXPIRY_BUFFER_SECONDS`, `DEFAULT_TOKEN_EXPIRY_SECONDS`

5. Define the AI Model Parameters constants:
   - `DEFAULT_MAX_TOKENS`, `PRD_MAX_TOKENS`, `DEFAULT_TEMPERATURE`, etc.

6. Define the Code Analysis & Chunking constants:
   - `MAX_CHUNK_SIZE_LINES`, `MIN_CHUNK_SIZE_LINES`, `CHUNK_OVERLAP_LINES`

7. Define the Cache Configuration constants:
   - `DEFAULT_CACHE_TTL_SECONDS`, `CACHE_PATH_HASH_LENGTH`

8. Define the File Processing constants:
   - `MAX_FILE_SIZE_BYTES`, `DEFAULT_FILE_ENCODING`, `SUPPORTED_EXTENSIONS`

9. Define the Visualization constants:
   - `DEFAULT_DEPENDENCY_MAX_DEPTH`, `KROKI_API_BASE_URL`, `MERMAID_COMPRESSION_LEVEL`

10. Define the QA Sentry constants:
    - Severity levels and scan types

11. Define the HTTP Status Codes constants:
    - Server error ranges, rate limit, and success codes

12. Save the file.

### Expected Outcomes
- A Python file containing well-defined application constants.
- Constants organized into logical sections for better readability.
- Magic numbers throughout the codebase replaced with meaningful constant names.

### Tips
- Use descriptive names for the constants.
- Group related constants together in logical sections.
- Add comments or docstrings to explain the purpose of each constant.
- Use uppercase names for constants to follow Python naming conventions.

### Warnings
- Be cautious when modifying the constants, as they may affect the entire codebase.
- Ensure that the constants are properly documented.
- If constants are used in multiple files, import them consistently.
- Avoid hardcoding values directly in the code.

## Tutorial

### Learning Objectives
1. Understand the purpose and benefits of centralizing configuration values.
2. Learn how to define and use constants for various application aspects.
3. Gain familiarity with common configuration values and their recommended defaults.
4. Practice applying configuration constants to improve code readability and maintainability.

### Prerequisites
- Basic understanding of Python syntax and concepts
- Familiarity with Python modules and importing
- Knowledge of HTTP and network concepts (optional)

### Step-by-Step Lessons

**Lesson 1: Introduction to Application Constants**
- Explain the concept of application constants and their purpose.
- Discuss the benefits of centralizing configuration values.

**Lesson 2-10: Configuration Sections**
- Explore each configuration section (HTTP & Network, Token & Authentication, AI Model Parameters, etc.)
- Discuss the purpose of each constant
- Explain how these constants can be used in practice

### Practice Exercises
1. Modify the HTTP_TIMEOUT_SECONDS constant and observe the impact.
2. Experiment with different values for DEFAULT_MAX_TOKENS.
3. Adjust the MAX_CHUNK_SIZE_LINES constant and analyze the impact.
4. Change the DEFAULT_CACHE_TTL_SECONDS value and observe cache behavior.
5. Customize the SUPPORTED_EXTENSIONS dictionary for your project.

### Summary
- Application constants provide a centralized location for configuration values.
- Centralizing constants improves code readability, maintainability, and consistency.
- The code demonstrates comprehensive configuration constants for various application aspects.

### Next Steps
- Explore the specific use cases of your Python application.
- Identify relevant configuration constants that align with your needs.
- Customize the values based on your specific requirements.
- Integrate the configuration constants into your codebase.
- Regularly review and update the configuration constants.

## Troubleshooting Guide

### Common Errors and Solutions

1. **KeyError: Missing Configuration Value**
   - Solution: Ensure all required configuration values are defined.

2. **TypeError: Invalid Operation on Configuration Value**
   - Solution: Verify the type of each configuration value.

3. **ValueError: Out of Range Configuration Value**
   - Solution: Validate configuration values against expected ranges.

4. **ImportError: Missing Module for Configuration**
   - Solution: Ensure all necessary modules are imported.

5. **SyntaxError: Invalid Configuration Syntax**
   - Solution: Review the syntax of the configuration values.

### Debugging Steps
1. Check for typos in configuration keys
2. Print configuration values to verify they're set correctly
3. Validate external dependencies
4. Review type conversions
5. Consult documentation

### FAQ

**Q: How can I add a new configuration value?**
A: Define the new constant at the appropriate section, following the existing structure.

**Q: What should I do if I need to change a configuration constant?**
A: Locate the constant and update its value. Test thoroughly and ensure consistency.

**Q: How can I make configuration values dynamic?**
A: Consider loading values from environment variables, configuration files, or databases.

### Known Issues
- Excessive logging of configuration values can impact performance.
- Changes in external systems may require updates to configuration values.

### Support Resources
- Internal documentation or wikis
- Development team consultation
- Code review processes
- External libraries documentation

## Requirements Specification

### Functional Requirements
1. The application should use centralized configuration for all constants.
2. The application should have configurable HTTP timeout for API requests.
3. The application should implement exponential backoff retry logic.
4. The application should handle token expiration with buffer time.
5. The application should have configurable AI model parameters.
6. The application should have configurable code analysis and chunking settings.
7. The application should have default cache TTL and configurable cache settings.
8. The application should have maximum file size limit and default encoding.
9. The application should support code analysis for various programming languages.
10. The application should have configurable visualization settings.
11. The application should have configurable severity levels for code issues.
12. The application should have predefined HTTP status codes for retry logic.

### Non-functional Requirements
1. The application should be configurable and maintainable.
2. The application should have a well-defined structure for configuration values.
3. The application should be extensible for future additions.
4. The application should have clear documentation for each constant.

### System Constraints
1. The application should be implemented in Python.
2. The application should not introduce security vulnerabilities.
3. The application should be compatible with supported programming languages.

### Dependencies
1. Python programming language and its standard libraries.
2. External libraries or APIs for specific functionalities (e.g., Kroki API).

### Acceptance Criteria
1. Clear and organized structure for configuration constants.
2. Centralized location for all configuration values.
3. Well-defined and configurable values for all aspects.
4. Thoroughly tested to ensure correct application of constants.
5. Comprehensive documentation for each configuration constant.