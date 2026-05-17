# Comprehensive Documentation for logging.py
**File:** mcp_server/lib/utils/logging.py
**Language:** Python
**Documentation type:** Comprehensive Documentation
**Generated:** 2026-05-17T09:32:53.669396Z

---

## API Documentation

# Endpoints/Functions

## `MCPLogger`
- **Constructor**: `__init__(self, name: str = "bobsuite-mcp", log_file: Optional[Path] = None)`
  - **Parameters**:
    - `name` (str): Logger name. Default is `"bobsuite-mcp"`.
    - `log_file` (Optional[Path]): Optional path to log file. Default is `None`.
  - **Description**: Initializes the logger with a specified name and optional log file. Removes any existing handlers and sets up a stderr handler with a formatter. Optionally adds a file handler if a log file is specified.
  
- **Methods**:
  - `debug(self, message: str, **kwargs)`: Logs a debug message.
    - **Parameters**:
      - `message` (str): Debug message.
      - `kwargs` (dict): Additional keyword arguments for extra information.
  - `info(self, message: str, **kwargs)`: Logs an info message.
    - **Parameters**:
      - `message` (str): Info message.
      - `kwargs` (dict): Additional keyword arguments for extra information.
  - `warning(self, message: str, **kwargs)`: Logs a warning message.
    - **Parameters**:
      - `message` (str): Warning message.
      - `kwargs` (dict): Additional keyword arguments for extra information.
  - `error(self, message: str, exc_info: bool = False, **kwargs)`: Logs an error message.
    - **Parameters**:
      - `message` (str): Error message.
      - `exc_info` (bool): Whether to include exception information. Default is `False`.
      - `kwargs` (dict): Additional keyword arguments for extra information.
  - `critical(self, message: str, exc_info: bool = False, **kwargs)`: Logs a critical message.
    - **Parameters**:
      - `message` (str): Critical message.
      - `exc_info` (bool): Whether to include exception information. Default is `False`.
      - `kwargs` (dict): Additional keyword arguments for extra information.
  - `exception(self, message: str, **kwargs)`: Logs an exception with traceback.
    - **Parameters**:
      - `message` (str): Exception message.
      - `kwargs` (dict): Additional keyword arguments for extra information.

## Global Logger Functions

- `get_logger(name: str = "bobsuite-mcp", log_file: Optional[Path] = None) -> MCPLogger`: Gets or creates the global logger instance.
  - **Parameters**:
    - `name` (str): Logger name. Default is `"bobsuite-mcp"`.
    - `log_file` (Optional[Path]): Optional path to log file. Default is `None`.
  - **Returns**: `MCPLogger` instance.
  
- `init_logger(name: str = "bobsuite-mcp", log_file: Optional[Path] = None) -> MCPLogger`: Initializes the global logger (useful for testing or resetting).
  - **Parameters**:
    - `name` (str): Logger name. Default is `"bobsuite-mcp"`.
    - `log_file` (Optional[Path]): Optional path to log file. Default is `None`.
  - **Returns**: `MCPLogger` instance.

## Convenience Functions

- `debug(message: str, **kwargs)`: Quick debug log.
- `info(message: str, **kwargs)`: Quick info log.
- `warning(message: str, **kwargs)`: Quick warning log.
- `error(message: str, exc_info: bool = False, **kwargs)`: Quick error log.
- `critical(message: str, exc_info: bool = False, **kwargs)`: Quick critical log.
- `exception(message: str, **kwargs)`: Quick exception log with traceback.

# Usage Examples

## Creating and Using an MCPLogger Instance

```python
from pathlib import Path
from mcp_logger import MCPLogger

# Create an MCPLogger instance
logger = MCPLogger(name="my-server", log_file=Path("logs/my_server.log"))

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
logger.exception("This is an exception message")
```

## Using the Global Logger

```python
from mcp_logger import get_logger

# Get the global logger
logger = get_logger()

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
logger.exception("This is an exception message")
```

## Quick Logging

```python
from mcp_logger import debug, info, warning, error, critical, exception

# Quick debug log
debug("This is a debug message")

# Quick info log
info("This is an info message")

# Quick warning log
warning("This is a warning message")

# Quick error log
error("This is an error message")

# Quick critical log
critical("This is a critical message")

# Quick exception log with traceback
exception("This is an exception message")
```

## Quick Start Guide

# Minimal setup steps

1. Ensure Python 3.6+ is installed on your system.
2. Install the required dependencies (if any) using pip. In this case, no external dependencies are required.

# Basic usage example

1. Import the `get_logger` function from the provided code.
2. Call `get_logger()` to obtain an instance of the `MCPLogger` class.
3. Use the available logging methods (`debug`, `info`, `warning`, `error`, `critical`, `exception`) to log messages.

Example:
```python
from mcp_logger import get_logger

logger = get_logger()

logger.info("Server started")
logger.debug("Processing request", request_id=123)
logger.warning("Low disk space", disk_usage=95)
logger.error("Failed to connect to database", exc_info=True)
```

# Next steps

1. Customize the logger by providing a custom name or log file path when calling `get_logger()`.
2. Utilize the provided convenience functions (`debug`, `info`, `warning`, `error`, `critical`, `exception`) for quick logging.
3. Integrate the logger into your MCP server application to log relevant information.

# Links to detailed documentation

- Python Logging Module: https://docs.python.org/3/library/logging.html
- Pathlib Module: https://docs.python.org/3/library/pathlib.html
- Datetime Module: https://docs.python.org/3/library/datetime.html

## User Manual

## Overview and Purpose
The `MCPLogger` module provides a logging utility specifically designed for MCP (Multi-Channel Protocol) servers. The primary purpose of this logger is to write log messages to `stderr` to avoid interfering with the standard input/output (stdio) communication between the MCP server and its clients. This is crucial because MCP servers utilize `stdin` and `stdout` for their primary communication, and any logging that uses `print()` statements or writes to `stdout` could corrupt the MCP protocol messages.

## Installation Instructions
To use the `MCPLogger` module, you need to have Python installed on your system. This module does not require any external dependencies beyond the Python Standard Library. You can directly copy the provided code into your project or install it as a package if packaged accordingly.

## Configuration Options
The `MCPLogger` class can be configured during initialization with the following parameters:
- `name`: The name of the logger. Defaults to `"bobsuite-mcp"`.
- `log_file`: An optional `Path` object specifying the file path where logs should be written. If not specified, logs will only be written to `stderr`.

## Usage Examples
### Basic Usage
```python
from mcp_logger import get_logger

# Get the global logger instance
logger = get_logger()

# Log an info message
logger.info("This is an info message")

# Log a debug message with extra information
logger.debug("This is a debug message", extra_info="debugging")
```

### Logging to a File
```python
from mcp_logger import get_logger
from pathlib import Path

# Specify a log file
log_file = Path("my_log_file.log")

# Get the global logger instance with file logging
logger = get_logger(log_file=log_file)

# Log messages
logger.info("This message will be logged to both stderr and the specified file")
```

## Common Use Cases
- **Server Monitoring**: Use the logger to monitor server activities, including errors and warnings, which can be crucial for troubleshooting and maintenance.
- **Debugging**: The debug logging level can be particularly useful during development or when diagnosing issues in a production environment.
- **Audit Trails**: Logging to a file can serve as an audit trail for actions performed by the server, which is useful for compliance and security purposes.

## Best Practices
- **Separate Concerns**: Use different log levels (`debug`, `info`, `warning`, `error`, `critical`) appropriately to separate different types of messages. This helps in filtering and focusing on specific types of log messages when needed.
- **Use Extra Information**: When logging messages, utilize the `**kwargs` to pass extra information. This can provide context to the log message, making it more informative.
- **File Logging**: For production environments, consider logging to a file in addition to `stderr`. This ensures that logs are preserved for future reference and analysis.
- **Global Logger**: Utilize the global logger instance provided by `get_logger()` to maintain a consistent logging setup across your application. This helps in avoiding the creation of multiple logger instances that might have conflicting configurations.

## How-To Guide

Objective:
The provided code is a Python module that defines a custom logger class `MCPLogger` and utility functions for logging messages in a specific format to stderr and optionally to a log file. The purpose of this logger is to avoid interfering with the standard input/output communication (stdin/stdout) used by MCP (Message Control Protocol) servers.

Prerequisites:
- Python 3.x
- Access to the file system for creating log files (if specified)
- Basic understanding of Python logging module

Step-by-step instructions:
1. Import the necessary modules
2. Define the `MCPLogger` class with initialization and logging methods
3. Create a global logger instance
4. Define convenience functions for quick logging

Expected outcomes:
- The `MCPLogger` class provides a custom logger that writes log messages to stderr and optionally to a log file.
- The logger avoids interfering with the stdin/stdout communication used by MCP servers.
- The logger supports different log levels and formats the log messages with a specific format and date format.

Tips and warnings:
- Make sure to import the necessary modules before using the `MCPLogger` class or the convenience functions.
- When creating an instance of `MCPLogger`, provide a meaningful name for the logger to identify it in the log messages.
- If you want to log messages to a file, make sure to provide a valid file path when initializing the logger.
- Be cautious when using the `exception` method, as it logs the exception message along with the traceback.

## Tutorial

## Learning Objectives

1. Understand the purpose and functionality of the `MCPLogger` class.
2. Learn how to use the `MCPLogger` class for logging messages in a Python application.
3. Understand how to configure the logger with a custom name and log file path.
4. Learn how to use convenience functions for quick logging.

## Prerequisites

- Basic knowledge of Python programming.
- Familiarity with the `logging` module in Python.

## Step-by-Step Lessons

### Lesson 1: Introduction to `MCPLogger`

The `MCPLogger` class is a custom logger that writes log messages to `stderr` to avoid interfering with the standard input/output communication used by MCP servers. It provides methods for logging messages at different severity levels, such as debug, info, warning, error, and critical.

### Lesson 2: Initializing the Logger

To use the `MCPLogger` class, you need to create an instance of it. You can do this by calling the `get_logger()` function and providing a name for the logger and an optional log file path.

```python
logger = get_logger(name="my_logger", log_file=Path("my_log_file.log"))
```

### Lesson 3: Logging Messages

Once you have a logger instance, you can use its methods to log messages at different severity levels.

### Lesson 4: Using Convenience Functions

The code provides convenience functions for quick logging without explicitly creating a logger instance.

## Troubleshooting Guide

### Common Errors and Solutions

1. **ImportError: No module named 'pathlib'**
   - **Solution**: Ensure you are using Python 3.4 or later. `pathlib` is a built-in module in Python 3.4+.

2. **PermissionError: [Errno 13] Permission denied**
   - **Solution**: This error occurs when the script does not have write permissions to the specified log file or directory. Ensure the script has the necessary permissions or choose a different log file location.

### Debugging Steps

1. **Check Python Version**: Verify that you are using Python 3.4 or later
2. **Verify Directory Permissions**: Ensure write permissions to the log directory
3. **Print Debug Information**: Add print statements to check variable values
4. **Use Python Debugger (pdb)**: Step through execution to inspect variables

### FAQ

1. **How do I change the log file location?**
   - You can specify a custom log file location by passing a `Path` object to the `get_logger()` or `init_logger()` function.

2. **How do I enable debug logging?**
   - By default, the logger is set to `INFO` level. To enable debug logging, change the log level to `DEBUG`.

3. **How do I log to a file without printing to stderr?**
   - Remove the `stderr_handler` from the `MCPLogger` class initialization.

### Known Issues

1. **Thread Safety**: The current implementation is not thread-safe. Consider using thread-safe logging configuration for multi-threaded applications.

2. **Log File Rotation**: The current implementation does not support log file rotation. Consider using `RotatingFileHandler` or `TimedRotatingFileHandler` for production use.

## Requirements Specification

Software Requirements Specification (SRS)

1. Introduction
1.1 Purpose
The purpose of this document is to specify the software requirements for the MCPLogger module, which provides logging utilities for the MCP Server. The logger writes log messages to stderr to avoid interfering with stdio communication between the MCP server and its clients.

1.2 Scope
This SRS covers the functional and non-functional requirements, system constraints, dependencies, and acceptance criteria for the MCPLogger module.

2. Overall Description
2.1 Product Perspective
The MCPLogger module is a standalone logging utility that can be used within the MCP Server application. It provides a logger instance that can be accessed globally or instantiated separately.

2.2 Product Functions
- Logging messages to stderr
- Optionally logging messages to a file
- Supporting different log levels (debug, info, warning, error, critical)
- Including timestamp, log level, logger name, and message in log output
- Allowing additional keyword arguments to be included in log messages

3. Specific Requirements
3.1 Functional Requirements
3.1.1 Logging to stderr
- The logger must write all log messages to stderr to avoid interfering with stdio communication.
- The logger must provide methods for logging messages at different levels.

3.1.2 Optional File Logging
- The logger must support optional logging to a specified file.
- If a log file is specified, the logger must create the necessary directories if they don't exist.

3.1.3 Log Message Formatting
- Log messages must include a timestamp, log level, logger name, and the actual message.
- Additional keyword arguments must be included in the log message.

3.2 Non-Functional Requirements
3.2.1 Performance
- The logger must not introduce significant overhead to the MCP Server application.

3.2.2 Maintainability
- The logger module must be well-structured, modular, and easy to maintain.

3.2.3 Compatibility
- The logger must be compatible with Python 3.x versions.

3.3 System Constraints
- The logger must be compatible with the operating systems supported by the MCP Server application.

3.4 Dependencies
- sys
- logging
- datetime
- pathlib

3.5 Acceptance Criteria
- The logger must successfully write log messages to stderr.
- The logger must support optional logging to a specified file.
- Log messages must include the required information.
- The global logger instance must be created only once and reused.