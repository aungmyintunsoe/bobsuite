# MCP Server Logging and Error Tracking

## Overview

This document explains the logging infrastructure implemented for the BobSuite MCP Server and how it solves the issues with `print()` statements interfering with stdio communication.

## The Problem

### Why `print()` Statements Break MCP Servers

MCP (Model Context Protocol) servers communicate via **stdin/stdout** using a structured JSON-RPC protocol. When you use `print()` statements in an MCP server:

1. **Protocol Corruption**: `print()` writes to stdout, which is the same channel used for MCP protocol messages
2. **Message Parsing Failures**: The MCP client expects valid JSON-RPC messages on stdout, but gets mixed with print output
3. **Hidden Errors**: Exceptions and errors get printed to stdout and are lost or corrupt the protocol
4. **No Error Tracking**: Without proper logging, debugging becomes nearly impossible

### Previous State

The codebase had **130+ `print()` statements** scattered across:
- Test files (acceptable - tests don't run as MCP servers)
- Core server code (problematic)
- Library modules (problematic)
- Utility functions (problematic)

## The Solution

### 1. Stderr-Based Logging System

Created [`mcp_server/lib/utils/logging.py`](mcp_server/lib/utils/logging.py) with:

```python
from lib.utils.logging import get_logger

logger = get_logger("my-module")
logger.info("This goes to stderr, not stdout")
logger.error("Errors are properly tracked", exc_info=True)
logger.exception("Full traceback captured")
```

**Key Features:**
- All logs go to **stderr** (not stdout)
- Structured logging with timestamps
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Optional file logging
- Exception tracking with full tracebacks
- Context-aware logging with kwargs

### 2. Implementation in Core Modules

#### Server.py
- Added comprehensive logging at initialization
- Tool execution logging with timing
- Full error tracking with tracebacks
- Startup/shutdown logging

```python
logger.info("Starting MCP server with stdio transport")
logger.debug(f"Calling tool: {name}", arguments=arguments)
logger.exception(f"Tool execution failed: {name}")
```

#### Ideation Engine (core.py)
- Step-by-step operation logging
- Validation error tracking
- PRD generation progress
- File save confirmation

```python
logger.info("Starting PRD synthesis", project_name=project_name)
logger.debug("Validating conversation data")
logger.exception("Error generating PRD with watsonx")
```

### 3. Error Response Enhancement

Enhanced error responses to include:
- Full exception tracebacks
- Error type information
- Context (tool name, arguments)
- Structured error data

```python
return self._error_response(
    str(e), 
    error_type=type(e).__name__, 
    tool_name=name, 
    arguments=arguments,
    traceback=tb  # Full traceback included
)
```

## Usage Guide

### Basic Logging

```python
from lib.utils.logging import get_logger

logger = get_logger("my-component")

# Different log levels
logger.debug("Detailed debugging info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
logger.critical("Critical failure", exc_info=True)

# With context
logger.info("Processing file", file_path="/path/to/file", size=1024)
```

### Exception Logging

```python
try:
    risky_operation()
except Exception as e:
    # Automatically captures full traceback
    logger.exception("Operation failed", operation="risky_operation")
    raise
```

### Quick Logging (Module-Level)

```python
from lib.utils import logging

logging.info("Quick log message")
logging.error("Quick error", exc_info=True)
```

## Log Output

### Console (stderr)
```
2026-05-17 16:18:25 [INFO] bobsuite-mcp-server: Initializing BobSuite MCP Server
2026-05-17 16:18:25 [INFO] ideation-engine: Initializing Ideation Engine
2026-05-17 16:18:25 [INFO] bobsuite-mcp-server: BobSuite MCP Server initialized successfully
2026-05-17 16:18:26 [INFO] bobsuite-mcp-server: Starting MCP server with stdio transport
2026-05-17 16:18:26 [INFO] bobsuite-mcp-server: MCP server running and ready to accept requests
```

### Log Files
Logs are automatically saved to: `mcp_server/logs/mcp_server_YYYYMMDD.log`

## Debugging with Logs

### Finding Errors

1. **Check stderr output** when running the MCP server
2. **Review log files** in `mcp_server/logs/`
3. **Look for EXCEPTION level** logs with full tracebacks
4. **Check ERROR responses** returned to IBM Bob

### Common Issues

#### Issue: AttributeError in synthesize_project_plan

**Before (Hidden):**
```
Error occurred somewhere... (lost in stdout)
```

**After (Visible):**
```
2026-05-17 16:20:15 [ERROR] ideation-engine: Error generating PRD with watsonx | error_type=AttributeError
Traceback (most recent call last):
  File "mcp_server/lib/ideation/core.py", line 150, in synthesize_prd
    prd_markdown = await self.watsonx.synthesize_prd(...)
  File "mcp_server/watsonx_client.py", line 123, in synthesize_prd
    result = response.get('results')[0].get('generated_text')
AttributeError: 'str' object has no attribute 'get'
```

## Test Files

**Note:** Test files (`mcp_server/tests/*.py`) still use `print()` statements. This is **intentional and correct** because:

1. Tests are run directly, not as MCP servers
2. Test output should go to stdout for visibility
3. Test frameworks expect stdout output
4. Tests don't communicate via MCP protocol

## Migration Status

### ✅ Completed
- [x] Created logging infrastructure
- [x] Updated `server.py` with comprehensive logging
- [x] Updated `lib/ideation/core.py` with step-by-step logging
- [x] Updated `lib/ideation/formatters.py` to use logging
- [x] Enhanced error responses with tracebacks
- [x] Exported logging utilities from `lib/utils/__init__.py`

### 📝 Remaining (Optional)
- [ ] Add logging to `lib/qa_sentry/` modules
- [ ] Add logging to `lib/autodocs/` modules
- [ ] Add logging to `lib/visualizer/` modules
- [ ] Add logging to `watsonx_client.py`

**Note:** The remaining modules can continue using their current error handling. The critical path (server.py and ideation engine) now has proper logging.

## Benefits

### Before
- ❌ Errors hidden or corrupt protocol
- ❌ No way to debug issues
- ❌ `print()` statements break MCP communication
- ❌ Stack traces lost

### After
- ✅ All errors captured to stderr
- ✅ Full tracebacks available
- ✅ MCP protocol remains clean
- ✅ Comprehensive debugging information
- ✅ Structured logging with context
- ✅ Automatic log file rotation

## Best Practices

1. **Always use logger, never print()** in MCP server code
2. **Include context** in log messages using kwargs
3. **Use appropriate log levels** (DEBUG for details, INFO for progress, ERROR for failures)
4. **Log exceptions with traceback** using `logger.exception()` or `exc_info=True`
5. **Keep test files using print()** - they don't run as MCP servers

## Troubleshooting

### Logs not appearing?
- Check that you're looking at **stderr**, not stdout
- Verify log file location: `mcp_server/logs/`
- Ensure logger is initialized: `logger = get_logger("module-name")`

### Still seeing print() statements?
- Check if it's in a test file (acceptable)
- Search for remaining print statements: `grep -r "print(" mcp_server/lib/`
- Replace with appropriate logger calls

### Need more detail?
- Change log level to DEBUG in `logging.py`
- Add more context to log calls: `logger.info("msg", key=value)`
- Enable file logging for persistent records

## Summary

The logging infrastructure ensures that:
1. **MCP protocol stays clean** - no stdout pollution
2. **Errors are visible** - all logs go to stderr
3. **Debugging is possible** - full tracebacks captured
4. **Production ready** - structured, searchable logs

This solves the original issue where errors in `synthesize_project_plan` were being caught somewhere without proper traceback display.