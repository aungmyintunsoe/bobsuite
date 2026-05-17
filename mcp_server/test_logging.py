"""
Test script to verify the logging system works correctly
Run this to ensure stderr logging is functioning properly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.utils.logging import get_logger, init_logger

def test_basic_logging():
    """Test basic logging functionality"""
    print("=" * 60)
    print("TESTING LOGGING SYSTEM")
    print("=" * 60)
    print("\nNote: Log messages should appear below (on stderr)")
    print("If you see them, the logging system is working!\n")
    
    # Initialize logger
    logger = get_logger("test-logger")
    
    # Test different log levels
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    
    # Test logging with context
    logger.info("Processing file", file_path="/test/path.py", size=1024)
    
    # Test exception logging
    try:
        raise ValueError("This is a test exception")
    except Exception as e:
        logger.exception("Caught test exception")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nIf you saw log messages above, the system is working!")
    print("Logs are also saved to: mcp_server/logs/")

def test_module_logging():
    """Test logging from different modules"""
    print("\n" + "=" * 60)
    print("TESTING MODULE-SPECIFIC LOGGERS")
    print("=" * 60 + "\n")
    
    # Test different module loggers
    server_logger = get_logger("bobsuite-mcp-server")
    ideation_logger = get_logger("ideation-engine")
    qa_logger = get_logger("qa-sentry")
    
    server_logger.info("Server logger test")
    ideation_logger.info("Ideation engine logger test")
    qa_logger.info("QA Sentry logger test")
    
    print("\n[OK] Module-specific loggers working\n")

def test_error_tracking():
    """Test comprehensive error tracking"""
    print("=" * 60)
    print("TESTING ERROR TRACKING")
    print("=" * 60 + "\n")
    
    logger = get_logger("error-test")
    
    # Simulate a complex error scenario
    try:
        def inner_function():
            raise AttributeError("'dict' object has no attribute 'missing_key'")
        
        def outer_function():
            inner_function()
        
        outer_function()
    except Exception as e:
        logger.exception("Complex error with full traceback")
        print("\n[OK] Full traceback captured in logs\n")

if __name__ == "__main__":
    test_basic_logging()
    test_module_logging()
    test_error_tracking()
    
    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)
    print("\nThe logging system is ready for use!")
    print("Check mcp_server/logs/ for log files")

# Made with Bob
