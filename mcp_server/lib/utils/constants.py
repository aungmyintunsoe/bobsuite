"""
Application Constants
Centralized configuration values to eliminate magic numbers throughout the codebase.
"""

# ============================================================================
# HTTP & NETWORK CONFIGURATION
# ============================================================================

# HTTP timeout in seconds for API requests
HTTP_TIMEOUT_SECONDS = 60.0

# Maximum number of retry attempts for transient failures
MAX_RETRY_ATTEMPTS = 3

# Base delay for exponential backoff (in seconds)
RETRY_BASE_DELAY_SECONDS = 1.0


# ============================================================================
# TOKEN & AUTHENTICATION
# ============================================================================

# Token expiration buffer in seconds (refresh 60s before actual expiry)
TOKEN_EXPIRY_BUFFER_SECONDS = 60

# Default token expiration time if not provided by API (in seconds)
DEFAULT_TOKEN_EXPIRY_SECONDS = 3600


# ============================================================================
# AI MODEL PARAMETERS
# ============================================================================

# Default maximum tokens for text generation
DEFAULT_MAX_TOKENS = 2000

# Maximum tokens for PRD synthesis (longer documents)
PRD_MAX_TOKENS = 4000

# Default temperature for balanced creativity/structure
DEFAULT_TEMPERATURE = 0.7

# Temperature for PRD synthesis (more structured)
PRD_TEMPERATURE = 0.4

# Temperature for code analysis (more deterministic)
CODE_ANALYSIS_TEMPERATURE = 0.1


# ============================================================================
# CODE ANALYSIS & CHUNKING
# ============================================================================

# Maximum lines per code chunk for analysis
MAX_CHUNK_SIZE_LINES = 1000

# Minimum lines to consider for chunking
MIN_CHUNK_SIZE_LINES = 100

# Overlap between chunks (in lines)
CHUNK_OVERLAP_LINES = 50


# ============================================================================
# CACHE CONFIGURATION
# ============================================================================

# Default cache TTL in seconds (1 hour)
DEFAULT_CACHE_TTL_SECONDS = 3600

# Cache key path hash length (characters)
CACHE_PATH_HASH_LENGTH = 8


# ============================================================================
# FILE PROCESSING
# ============================================================================

# Maximum file size for processing (in bytes) - 10MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

# Default encoding for file operations
DEFAULT_FILE_ENCODING = 'utf-8'

# Supported file extensions for code analysis (maps extension to language name)
SUPPORTED_EXTENSIONS = {
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.jsx': 'JavaScript',
    '.tsx': 'TypeScript', '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.h': 'C',
    '.hpp': 'C++', '.cs': 'C#', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby',
    '.php': 'PHP', '.swift': 'Swift', '.kt': 'Kotlin', '.scala': 'Scala', '.r': 'R',
    '.m': 'Objective-C', '.mm': 'Objective-C++', '.sh': 'Shell', '.bash': 'Bash',
    '.zsh': 'Zsh', '.ps1': 'PowerShell', '.sql': 'SQL', '.html': 'HTML', '.css': 'CSS',
    '.scss': 'SCSS', '.sass': 'Sass', '.less': 'Less', '.vue': 'Vue', '.svelte': 'Svelte',
    '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML', '.xml': 'XML', '.md': 'Markdown',
    '.txt': 'Text', '.toml': 'TOML', '.ini': 'INI', '.cfg': 'Config', '.conf': 'Config'
}


# ============================================================================
# VISUALIZATION
# ============================================================================

# Default maximum depth for dependency analysis
DEFAULT_DEPENDENCY_MAX_DEPTH = 3

# Kroki API base URL for diagram generation
KROKI_API_BASE_URL = "https://kroki.io"

# Compression level for Mermaid diagrams (1-9, 9 is maximum)
MERMAID_COMPRESSION_LEVEL = 9


# ============================================================================
# QA SENTRY
# ============================================================================

# Severity levels for code issues
SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"

# Default scan types
SCAN_TYPE_ALL = "all"
SCAN_TYPE_SECURITY = "security"
SCAN_TYPE_PERFORMANCE = "performance"
SCAN_TYPE_STYLE = "style"


# ============================================================================
# HTTP STATUS CODES (for retry logic)
# ============================================================================

# Server error status codes (retryable)
HTTP_STATUS_SERVER_ERROR_MIN = 500
HTTP_STATUS_SERVER_ERROR_MAX = 599

# Rate limit status code (retryable)
HTTP_STATUS_RATE_LIMIT = 429

# Success status code
HTTP_STATUS_OK = 200


# Made with Bob
