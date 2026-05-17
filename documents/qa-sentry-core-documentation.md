# Comprehensive Documentation for QA Sentry Core
**File:** mcp_server/lib/qa_sentry/core.py
**Language:** Python
**Documentation type:** Comprehensive Documentation
**Generated:** 2026-05-17T09:22:18.422151Z

---

## API Documentation

### QASentry Class

Main orchestrator class for code quality analysis using multi-agent AI scanning.

#### Methods

**`__init__(client, enable_cache=True)`**
- Initialize QA Sentry with WatsonX client
- Parameters:
  - `client`: WatsonXClient instance
  - `enable_cache`: Enable/disable caching (default: True)

**`async scan_code(file_path, scan_type="all", auto_fix=False, additional_context="")`**
- Scan a single code file for issues
- Parameters:
  - `file_path`: Path to file to scan
  - `scan_type`: Type of scan ("bugs", "vulnerabilities", "quality", "all")
  - `auto_fix`: Apply automatic fixes (default: False)
  - `additional_context`: Additional context for analysis
- Returns: JSON scan results

**`async batch_scan(file_paths, scan_type="all", auto_fix=False)`**
- Scan multiple files concurrently
- Parameters:
  - `file_paths`: List of file paths
  - `scan_type`: Type of scan
  - `auto_fix`: Apply automatic fixes
- Returns: List of scan results

**`async scan_git_diff(repo_path, staged=True, max_files=10, max_file_size_kb=500)`**
- Scan only changed files from git diff
- Parameters:
  - `repo_path`: Path to git repository
  - `staged`: Scan staged changes (default: True)
  - `max_files`: Maximum files to scan
  - `max_file_size_kb`: Maximum file size in KB
- Returns: Scan results for changed files

**`async generate_unit_tests(file_path, testing_library="pytest", test_requirements="")`**
- Generate unit tests for a file
- Parameters:
  - `file_path`: Path to file
  - `testing_library`: Testing framework to use
  - `test_requirements`: Test requirements file
- Returns: Generated test code

**`async generate_network_performance_tests(file_path, testing_library="locust", test_requirements="")`**
- Generate network performance tests
- Parameters:
  - `file_path`: Path to file
  - `testing_library`: Testing framework
  - `test_requirements`: Test requirements
- Returns: Generated test code

**`generate_report(scan_results, output_path=None)`**
- Generate markdown report from scan results
- Parameters:
  - `scan_results`: List of scan results
  - `output_path`: Optional output file path
- Returns: Markdown report string

---

## Quick Start Guide

### Minimal Setup Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create WatsonX client instance**
   ```python
   from lib.utils.watsonx import WatsonXClient
   watsonx_client = WatsonXClient(api_key="your_api_key")
   ```

3. **Initialize QA Sentry**
   ```python
   s = QASentry(watsonx_client)
   ```

### Basic Usage Example

```python
async def main():
    # Initialize
    s = QASentry(watsonx_client)
    
    # Scan a single file
    result = await s.scan_code("example.py")
    print(result)
    
    # Batch scan multiple files
    results = await s.batch_scan(["file1.py", "file2.py"])
    print(results)
    
    # Generate a report
    report = s.generate_report(results)
    print(report)
    
asyncio.run(main())
```

### Next Steps

1. Explore advanced configuration options in `prompts.py`
2. Customize test generation by modifying `test_persona.txt`
3. Integrate with CI/CD pipeline using batch scan functionality
4. Review detailed documentation for each module

### Detailed Documentation Links

- Agents: `lib/qa_sentry/agents.py`
- Chunking: `lib/qa_sentry/chunking.py`
- Auto Fixer: `lib/qa_sentry/auto_fixer.py`
- Git Utilities: `lib/qa_sentry/git_utils.py`
- Reporting: `lib/qa_sentry/reporting.py`

---

## User Manual

### Overview and Purpose

QA Sentry is a production-grade code quality analysis tool using multi-agent AI with debate pattern (Finder vs. Critic). It provides comprehensive code analysis, automatic test generation, and detailed reporting.

### Configuration Options

**Environment Variables:**
- `QASENTRY_CACHE`: Enable/disable cache (default: true)
- `QASENTRY_CHUNK_SIZE`: Override default chunk size (default: 1000)
- `QASENTRY_MAX_TOKENS`: Override default max tokens (default: 4000)
- `QASENTRY_TEMPERATURE`: Override default temperature (default: 0.1)

**Command Line Options:**
- `--cache`: Enable/disable cache
- `--chunk-size`: Set chunk size
- `--max-tokens`: Set max tokens
- `--temperature`: Set temperature

### Common Use Cases

1. **Full production scan with auto-fix:**
   ```python
   qasentry.scan_code("./app.py", scan_type="all", auto_fix=True)
   ```

2. **Quality scan for multiple files:**
   ```python
   qasentry.batch_scan(["./service1.py", "./service2.py"], scan_type="quality")
   ```

3. **Scan only changed files in git repo:**
   ```python
   qasentry.scan_git_diff(repo_path="./my_project", staged=False)
   ```

4. **Generate network performance tests:**
   ```python
   qasentry.generate_network_performance_tests("./service.py", testing_library="locust")
   ```

5. **Generate unit tests with custom requirements:**
   ```python
   qasentry.generate_unit_tests(
       file_path="./utils.py",
       testing_library="pytest",
       test_requirements="test_requirements.txt"
   )
   ```

### Best Practices

1. Always use cache in production for performance gains
2. Use batch_scan for large projects for faster execution
3. Set max_file_size_kb appropriately for large files
4. Run scans in controlled environment with limited permissions
5. Regularly update system prompt for latest security standards
6. Provide clear requirements in test_requirements files
7. Analyze files after commit but before merging
8. Review auto-fixes carefully before applying
9. Keep WatsonX model up to date
10. Monitor API usage to avoid unexpected costs
11. Break down scans into smaller batches for complex projects
12. Regularly review generated reports
13. Use --cache option in CI/CD pipelines
14. Contribute custom prompts to community
15. Keep QA Sentry installation updated

---

## How-To Guide

### Objective
Implement a production-grade code quality analysis tool using multi-agent AI with debate pattern.

### Prerequisites
- Python 3.9+ with asyncio support
- WatsonxClient instance configured
- Required libraries installed
- reviewer.txt or prompts/system_context.md for system prompt

### Step-by-Step Instructions

1. **Set up environment:**
   - Ensure Python 3.9+ is installed
   - Install required libraries
   - Configure WatsonxClient instance

2. **Initialize QASentry:**
   ```python
   from lib.qa_sentry.qa_sentry import QASentry
   watsonx_client = WatsonxClient()
   analyzer = QASentry(watsonx_client)
   ```

3. **Scan a single file:**
   ```python
   scan_results = await analyzer.scan_code("path/to/your/file.py", scan_type="all", auto_fix=False)
   print(scan_results)
   ```

4. **Batch scan multiple files:**
   ```python
   files = ["file1.py", "file2.py", "file3.py"]
   batch_results = await analyzer.batch_scan(files, scan_type="all", auto_fix=False)
   for result in batch_results:
       print(result)
   ```

5. **Scan changed files from git diff:**
   ```python
   git_results = await analyzer.scan_git_diff("/path/to/your/repo", staged=True, max_files=20)
   print(git_results)
   ```

6. **Generate tests:**
   ```python
   unit_tests = await analyzer.generate_unit_tests("path/to/your/file.py", testing_library="pytest")
   print(unit_tests)
   ```

7. **Generate a report:**
   ```python
   report = analyzer.generate_report(batch_results, output_path="qa_report.md")
   print(report)
   ```

### Expected Outcomes
- Comprehensive code analysis reports in JSON format
- Automatic test generation for various test types
- Markdown reports summarizing findings
- Optional automatic code fixes applied
- Cached results for improved performance

### Tips and Warnings
- Chunk size optimized at 1000 lines for reduced API calls
- File hash-based caching enabled by default
- Auto-fix modifies original files - use with caution
- For large projects, use batch_scan with additional context
- System prompt loaded from reviewer.txt or prompts/system_context.md
- Temperature set to 0.1 for strict technical mode
- Monitor API usage
- Ensure sufficient memory for large files
- Always review auto-fixes before committing
- Designed for Python but can analyze other languages
- Run batch scans concurrently with asyncio.gather()
- Regularly update library dependencies

---

## Tutorial

### Learning Objectives
1. Understand multi-agent AI code scanner architecture
2. Learn to orchestrate complex workflows with asyncio
3. Master large file chunking techniques
4. Implement caching strategies
5. Create production-grade code analysis pipelines
6. Generate dynamic tests
7. Produce structured reports

### Prerequisites
- Basic Python programming skills
- Familiarity with async/await
- Understanding of JSON data structures
- Knowledge of Git basics
- Experience with AI APIs
- Familiarity with code quality concepts

### Step-by-Step Lessons

**Step 1: Understanding the Architecture**
- Examine QASentry class and responsibilities
- Identify main components: agents, chunking, test_generator, reporting
- Understand debate pattern (Finder vs Critic)

**Step 2: Initializing the Scanner**
- Learn to create QASentry instance
- Explore initialization parameters
- Understand system prompts importance

**Step 3: Scanning Individual Files**
- Analyze scan_code method
- Understand file reading and error handling
- Learn about language detection
- Explore chunking logic
- Understand caching mechanism

**Step 4: Implementing the Debate Pattern**
- Study finder_pass and critic_pass functions
- Understand findings passing between agents
- Learn about two-pass analysis

**Step 5: Caching Mechanism**
- Examine cache implementation
- Understand cache key generation
- Learn about cache hit/miss logic

**Step 6: Auto-Fix Feature**
- Explore apply_auto_fixes function
- Understand how fixes are applied
- Learn about integration with scan_code

**Step 7: Git Diff Scanning**
- Study scan_git_diff method
- Understand git diff processing
- Learn about configurable limits

**Step 8: Batch Scanning**
- Analyze batch_scan method
- Understand concurrent execution
- Learn about cross-file context building

**Step 9: Test Generation**
- Explore test generation methods
- Understand different test types
- Learn about test_requirements parameter

**Step 10: Reporting**
- Study generate_report method
- Understand markdown report structure
- Learn about output options

### Practice Exercises

1. **Customizing System Prompt**
   - Modify _load_system_context method
   - Create custom prompt file
   - Test how custom prompt affects results

2. **Implementing New Test Type**
   - Add new test_type (e.g., "security")
   - Implement logic in test_generator
   - Modify generate_tests method
   - Test implementation

3. **Optimizing Cache Usage**
   - Analyze current caching mechanism
   - Implement sophisticated cache key generation
   - Test cache hit rates
   - Measure performance improvements

4. **Adding New Agent**
   - Create "reviewer" agent for third pass
   - Implement reviewer_pass function
   - Integrate into scan_code workflow
   - Test additional analysis effects

5. **Implementing Batch Auto-Fix**
   - Modify batch_scan for auto-fixes
   - Implement error handling
   - Test with files containing known issues

### Summary
You've learned how to build and use a comprehensive code quality analysis system with multi-agent AI scanning, including architecture, workflow orchestration, file handling, caching, pipelines, test generation, and reporting.

### Next Steps
1. Experiment with different AI models
2. Integrate with CI/CD pipeline
3. Create custom test personas
4. Explore advanced AI prompting techniques
5. Contribute to open-source community
6. Study component documentation
7. Implement visualization dashboard

---

## Troubleshooting Guide

### Common Errors and Solutions

1. **FileNotFoundError**
   - Description: File path is incorrect or file doesn't exist
   - Solution: Verify file_path is correct and file exists

2. **PermissionError**
   - Description: Insufficient permissions to read file
   - Solution: Ensure process has read permissions

3. **WatsonXClientError**
   - Description: Error communicating with WatsonX AI service
   - Solution: Check service status, API keys, and network connectivity

4. **AsyncioTimeoutError**
   - Description: Timeout during AI analysis
   - Solution: Increase max_tokens or reduce chunk_size

5. **JSONDecodeError**
   - Description: Invalid JSON output from AI model
   - Solution: Check system_prompt formatting and JSON schema

6. **RecursionError**
   - Description: Excessive recursion during deep analysis
   - Solution: Reduce chunk_size or simplify code structures

7. **CacheKeyCollision**
   - Description: Cache key collisions causing stale results
   - Solution: Ensure unique file paths and scan types

### Debugging Steps

1. Enable DEBUG logging: Set log_level='DEBUG'
2. Use --debug flag for verbose output
3. Isolate issue with single file
4. Check WatsonX service status
5. Verify system_prompt format
6. Run with --no-cache to bypass cache
7. Adjust temperature parameter (0.0-0.2)
8. Profile with: `python -m cProfile -o profile.out your_script.py`
9. Use built-in profiler
10. Report bugs with full traceback

### FAQ

**Q: How do I configure chunk size?**
A: Set via chunk_size attribute in QASentry class. Default is 1000 lines.

**Q: Can I disable caching?**
A: Yes, set enable_cache=False when initializing QASentry.

**Q: What file types are supported?**
A: QA Sentry auto-detects 100+ programming languages.

**Q: How do I customize system prompt?**
A: Modify reviewer.txt or system_context.md in prompts/ directory.

**Q: I'm getting 'Rate limit exceeded' errors. What should I do?**
A: Implement exponential backoff retry logic or contact WatsonX support.

**Q: How can I analyze multiple files concurrently?**
A: Use batch_scan method with asyncio.gather.

**Q: What's the difference between finder and critic passes?**
A: Finder identifies issues, critic validates and expands. This debate pattern improves accuracy.

**Q: Can I integrate with CI/CD pipelines?**
A: Yes, designed for CI/CD integration using scan_code or batch_scan methods.

### Known Issues

1. **False positives in pattern matching**
   - Description: AI might flag valid patterns as issues
   - Workaround: Adjust temperature to lower values or add exceptions in prompts

2. **Performance degradation with very large files (>10,000 lines)**
   - Description: Chunking may cause context loss
   - Workaround: Split files manually or implement custom chunking

3. **Cache not updating after code changes**
   - Description: Hash-based cache might not detect certain changes
   - Workaround: Use --no-cache flag or manually clear cache

4. **Compatibility issues with Python 3.6**
   - Description: Some features require Python 3.7+
   - Workaround: Upgrade to Python 3.7 or later

5. **AI service downtime causing pipeline failures**
   - Description: External AI service unavailability impacts analysis
   - Workaround: Implement retry logic or use local model fallback

### Support Resources

- **GitHub Repository**: https://github.com/bobcodeai/qasentry
- **Issue Tracker**: https://github.com/bobcodeai/qasentry/issues
- **Documentation**: https://qasentry.readthedocs.io
- **Community Forum**: https://forum.qasentry.ai
- **Support Email**: support@qasentry.ai
- **Slack Community**: https://slack.qasentry.ai
- **Contribution Guidelines**: https://github.com/bobcodeai/qasentry/blob/main/CONTRIBUTING.md
- **Code of Conduct**: https://github.com/bobcodeai/qasentry/blob/main/CODE_OF_CONDUCT.md

---

## Requirements Specification

### Functional Requirements

1. Must scan code files for bugs, vulnerabilities, and quality issues
2. Must support multiple scan types (bugs, vulnerabilities, quality, all)
3. Must provide automatic fix suggestions
4. Must support batch scanning of multiple files
5. Must scan git diff for changed files only
6. Must generate unit tests and network performance tests
7. Must produce structured JSON reports
8. Must generate markdown reports
9. Must implement caching for performance
10. Must support concurrent file processing

### Non-Functional Requirements

**Performance:**
- Process files >1000 lines within 30 seconds
- Achieve 2x speedup with concurrent batch scanning
- Cache hit rate >= 80% for repeated scans

**Reliability:**
- Handle file read errors gracefully
- Implement retry logic for API errors (max 3 attempts)
- Provide comprehensive error reporting

**Usability:**
- Provide clear error messages
- Allow configuration of chunk size, temperature, max tokens
- Support optional auto-fix with safety checks

**Maintainability:**
- Clear separation of concerns
- Type annotations for public methods
- Comprehensive docstrings

**Testability:**
- Unit tests for all public methods
- Mock external dependencies in tests
- Integration tests for full pipeline

**Extensibility:**
- Easy addition of new scan types
- Support custom system prompts
- Configurable analysis parameters

### System Constraints

**Performance Requirements:**
- Process files >1000 lines within 30 seconds on standard cloud VM
- Concurrent batch scanning achieves 2x speedup
- Cache hit rate >= 80%

**Security Constraints:**
- Must not execute code from scanned files
- All API calls through secure channels
- Redact sensitive information in reports

**Compatibility Requirements:**
- Support Python 3.7 to 3.12
- Handle Unix and Windows line endings
- Support UTF-8, UTF-16, and ASCII encoding

**Scalability Constraints:**
- Handle up to 1000 files concurrently
- Gracefully degrade with API rate limits

**Maintenance Requirements:**
- Centralized prompts in prompts.py
- Easily updatable system prompt
- Adhere to PEP 8 standards (max 120 chars)

### Dependencies

**Python Standard Library:**
- asyncio
- pathlib
- typing
- traceback

**Third-Party Libraries:**
- WatsonxClient (external AI client)
- lib.utils, lib.qa_sentry.* (internal modules)

**System Dependencies:**
- Python 3.7 or higher
- Access to Watsonx API
- Sufficient disk space for caching (10GB)

### Acceptance Criteria

**Functional Acceptance:**
- Produce JSON reports with specified schema
- Identify 90%+ of known vulnerabilities
- Auto-fix applies 80%+ of fixes correctly

**Performance Acceptance:**
- Process 5000-line file in <20 seconds
- Process 100 files in <2 minutes
- Cache reduces processing time by 50%+

**Quality Acceptance:**
- 90%+ code coverage in unit tests
- Pass pylint with 9/10 minimum score
- Generate human-readable, actionable reports

**Security Acceptance:**
- No sensitive information exposure without request
- Validate all inputs to prevent injection attacks

**Compatibility Acceptance:**
- Successfully scan Python 3.7-3.12 codebases
- Handle mixed line endings correctly
- Process UTF-8, UTF-16, and ASCII files

**Scalability Acceptance:**
- Handle 1000 file batch scan without crashing
- Gracefully handle API rate limit errors

**Maintainability Acceptance:**
- Updatable system prompt without code changes
- All prompts in single location
- Adhere to PEP 8 standards

**Extensibility Acceptance:**
- Add new scan types by implementing new methods
- Customize system prompt via constructor
- Adjust analysis temperature via constructor