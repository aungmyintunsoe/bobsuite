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

# Supported file extensions for code analysis
SUPPORTED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
    '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.r',
    '.m', '.mm', '.sh', '.bash', '.zsh', '.ps1', '.sql', '.html', '.css',
    '.scss', '.sass', '.less', '.vue', '.svelte', '.json', '.yaml', '.yml',
    '.xml', '.md', '.txt', '.toml', '.ini', '.cfg', '.conf'
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
