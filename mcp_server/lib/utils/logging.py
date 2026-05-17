"""
Logging utilities for MCP Server
Provides stderr-based logging that doesn't interfere with stdio communication
"""

import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class MCPLogger:
    """
    Logger that writes to stderr to avoid interfering with MCP stdio communication.
    
    MCP servers communicate via stdin/stdout, so all logging MUST go to stderr.
    Using print() statements will corrupt the MCP protocol messages.
    """
    
    def __init__(self, name: str = "bobsuite-mcp", log_file: Optional[Path] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        self.logger.handlers.clear()
        
        # Create stderr handler (required for MCP)
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        stderr_handler.setFormatter(formatter)
        self.logger.addHandler(stderr_handler)
        
        # Optionally add file handler
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        full_message = f"{message} {extra_info}".strip()
        self.logger.debug(full_message)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        full_message = f"{message} {extra_info}".strip()
        self.logger.info(full_message)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        full_message = f"{message} {extra_info}".strip()
        self.logger.warning(full_message)
    
    def error(self, message: str, exc_info: bool = False, **kwargs):
        """Log error message"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        full_message = f"{message} {extra_info}".strip()
        self.logger.error(full_message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False, **kwargs):
        """Log critical message"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        full_message = f"{message} {extra_info}".strip()
        self.logger.critical(full_message, exc_info=exc_info)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        full_message = f"{message} {extra_info}".strip()
        self.logger.exception(full_message)


# Global logger instance
_global_logger: Optional[MCPLogger] = None


def get_logger(name: str = "bobsuite-mcp", log_file: Optional[Path] = None) -> MCPLogger:
    """
    Get or create the global logger instance.
    
    Args:
        name: Logger name
        log_file: Optional path to log file
    
    Returns:
        MCPLogger instance
    """
    global _global_logger
    
    if _global_logger is None:
        # Default log file location
        if log_file is None:
            log_dir = Path(__file__).parent.parent.parent / "logs"
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / f"mcp_server_{datetime.now().strftime('%Y%m%d')}.log"
        
        _global_logger = MCPLogger(name, log_file)
    
    return _global_logger


def init_logger(name: str = "bobsuite-mcp", log_file: Optional[Path] = None) -> MCPLogger:
    """
    Initialize the global logger (useful for testing or resetting).
    
    Args:
        name: Logger name
        log_file: Optional path to log file
    
    Returns:
        MCPLogger instance
    """
    global _global_logger
    _global_logger = MCPLogger(name, log_file)
    return _global_logger


# Convenience functions for quick logging
def debug(message: str, **kwargs):
    """Quick debug log"""
    get_logger().debug(message, **kwargs)


def info(message: str, **kwargs):
    """Quick info log"""
    get_logger().info(message, **kwargs)


def warning(message: str, **kwargs):
    """Quick warning log"""
    get_logger().warning(message, **kwargs)


def error(message: str, exc_info: bool = False, **kwargs):
    """Quick error log"""
    get_logger().error(message, exc_info=exc_info, **kwargs)


def critical(message: str, exc_info: bool = False, **kwargs):
    """Quick critical log"""
    get_logger().critical(message, exc_info=exc_info, **kwargs)


def exception(message: str, **kwargs):
    """Quick exception log with traceback"""
    get_logger().exception(message, **kwargs)

# Made with Bob
