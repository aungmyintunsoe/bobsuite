# Bob Suite MCP Server - Test Suite

## Overview

This directory contains comprehensive unit and network tests for the Bob Suite MCP Server. All tests follow **Steve Sanderson's Unit Testing Principles** and are designed for maximum isolation, clarity, and maintainability.

## Quick Start

### Install Test Dependencies
```bash
pip install pytest pytest-asyncio pytest-mock pytest-benchmark
```

### Run All Tests
```bash
cd mcp_server/tests
pytest
```

### Run with Coverage
```bash
pytest --cov=mcp_server --cov-report=html
```

## Test Files

| File | Purpose | Tests | Lines |
|------|---------|-------|-------|
| `test_mcp_server.py` | MCP server handlers | 10 | 91 |
| `test_watsonx_client_network.py` | Network/API tests | 8 | 73 |
| `test_core_scanning.py` | QA Sentry core | 6 | 46 |
| `test_autodocs_core.py` | AutoDocs engine | 5 | 75 |
| `test_visualizer_core.py` | Visualizer engine | 9 | 109 |

**Total:** 38 tests across 5 files

## Running Tests

### Run Specific Test File
```bash
pytest test_mcp_server.py
pytest test_watsonx_client_network.py -v
```

### Run Specific Test
```bash
pytest test_mcp_server.py::test_scan_code_quality
pytest test_watsonx_client_network.py::test_api_connection
```

### Run with Different Output Levels
```bash
pytest -q              # Quiet mode
pytest -v              # Verbose mode
pytest -vv             # Extra verbose
pytest --tb=short      # Short traceback
pytest --tb=no         # No traceback
```

### Run Tests Matching Pattern
```bash
pytest -k "scan"       # Run tests with "scan" in name
pytest -k "network"    # Run tests with "network" in name
pytest -k "not slow"   # Skip tests marked as slow
```

### Run with Coverage Report
```bash
# Terminal report
pytest --cov=mcp_server --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=mcp_server --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=mcp_server --cov-report=xml
```

### Run Performance Benchmarks
```bash
pytest test_watsonx_client_network.py::test_performance --benchmark-only
```

## Environment Setup

### Required Environment Variables

For network tests to work properly, set these environment variables:

```bash
# Linux/Mac
export IBM_API_KEY="your-ibm-api-key"
export PROJECT_ID="your-watsonx-project-id"

# Windows PowerShell
$env:IBM_API_KEY="your-ibm-api-key"
$env:PROJECT_ID="your-watsonx-project-id"

# Windows CMD
set IBM_API_KEY=your-ibm-api-key
set PROJECT_ID=your-watsonx-project-id
```

### Optional: Create .env File
```bash
# Create .env file in mcp_server directory
echo "IBM_API_KEY=your-key" > ../mcp_server/.env
echo "PROJECT_ID=your-project-id" >> ../mcp_server/.env
```

## Test Structure

### Naming Convention (S/S/R)
All tests follow the **Subject/Scenario/Result** naming pattern:

```python
def test_scan_code_quality():
    # Subject: QASentry.scan_code
    # Scenario: Scanning Python file for quality issues
    # Result: Returns analysis with health score
```

### Test Organization
```
tests/
├── pytest.ini              # pytest configuration
├── README.md              # This file
├── TEST_SUMMARY.md        # Comprehensive test documentation
├── test_mcp_server.py     # MCP server handler tests
├── test_watsonx_client_network.py  # Network/API tests
├── test_core_scanning.py  # QA Sentry tests
├── test_autodocs_core.py  # AutoDocs tests
└── test_visualizer_core.py # Visualizer tests
```

## Test Principles

All tests adhere to Steve Sanderson's Unit Testing Principles:

1. ✅ **Absolute Orthogonality** - Tests are completely independent
2. ✅ **Single Logical Assertion** - One concept per test
3. ✅ **Isolation of the Unit** - External dependencies mocked
4. ✅ **Ruthless Mocking** - All external services mocked
5. ✅ **Zero Unnecessary Preconditions** - Minimal setup
6. ✅ **Strict S/S/R Naming** - Clear test names

## Mocking Strategy

### Mock External Dependencies
```python
from unittest.mock import AsyncMock, patch

# Mock async methods
watsonx_client = AsyncMock()

# Mock file operations
@patch('mcp_server.lib.utils.file_io.read_file_safe')
def test_something(mock_read):
    mock_read.return_value = ("content", None)
```

### Mock Patterns Used
- `AsyncMock()` - For async methods
- `@patch()` - For function/method patching
- `MagicMock()` - For general mocking
- `return_value` - For simple return values
- `side_effect` - For exceptions or sequences

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-asyncio pytest-mock pytest-cov
      - run: pytest --cov=mcp_server --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Troubleshooting

### Import Errors
If you see import errors for pytest:
```bash
pip install pytest pytest-asyncio pytest-mock
```

### Async Test Failures
Ensure pytest-asyncio is installed and configured:
```bash
pip install pytest-asyncio
```

Check `pytest.ini` has:
```ini
[pytest]
asyncio_mode = auto
```

### Network Test Failures
1. Check environment variables are set
2. Verify IBM Cloud API key is valid
3. Ensure network connectivity
4. Check WatsonX service status

### Coverage Not Working
Install pytest-cov:
```bash
pip install pytest-cov
```

## Test Coverage Goals

| Module | Target | Current |
|--------|--------|---------|
| server.py | 90% | TBD |
| watsonx_client.py | 85% | TBD |
| qa_sentry/core.py | 90% | TBD |
| autodocs/core.py | 90% | TBD |
| visualizer/core.py | 85% | TBD |

Run coverage to update:
```bash
pytest --cov=mcp_server --cov-report=term-missing
```

## Adding New Tests

### 1. Create Test File
```python
# test_new_feature.py
import pytest
from mcp_server.lib.new_feature import NewFeature

class TestNewFeature:
    @pytest.fixture
    def feature(self):
        return NewFeature()
    
    def test_feature_does_something(self, feature):
        # Subject: NewFeature.do_something
        # Scenario: Valid input provided
        # Result: Returns expected output
        result = feature.do_something("input")
        assert result == "expected"
```

### 2. Follow Naming Convention
- File: `test_*.py`
- Class: `TestClassName`
- Method: `test_subject_scenario_result`

### 3. Mock External Dependencies
```python
@patch('mcp_server.lib.external.service')
def test_with_mock(mock_service):
    mock_service.return_value = "mocked"
    # Test code here
```

### 4. Run Your New Tests
```bash
pytest test_new_feature.py -v
```

## Performance Testing

### Benchmark Tests
```bash
pytest test_watsonx_client_network.py::test_performance --benchmark-only
```

### Load Testing
```bash
pytest test_watsonx_client_network.py::test_concurrent_requests -v
```

## Documentation

- **Full Test Summary:** See [`TEST_SUMMARY.md`](./TEST_SUMMARY.md)
- **MCP Server Docs:** See [`../README.md`](../README.md)
- **Architecture:** See [`../ARCHITECTURE.md`](../ARCHITECTURE.md)

## Support

For issues or questions:
1. Check [`TEST_SUMMARY.md`](./TEST_SUMMARY.md) for detailed documentation
2. Review test output with `-vv` flag for more details
3. Check environment variables are set correctly
4. Verify all dependencies are installed

## License

Same as parent project - see [`../../LICENSE`](../../LICENSE)

---

**Generated:** 2026-05-17  
**Framework:** pytest  
**Principles:** Steve Sanderson Unit Testing Manifesto