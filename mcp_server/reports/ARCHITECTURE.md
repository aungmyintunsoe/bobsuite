# BobSuite MCP Server - Architecture Documentation

## Overview

BobSuite is a comprehensive code quality and documentation platform powered by IBM watsonx.ai. This document describes the system architecture, design decisions, and recent improvements.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Server (server.py)                   │
│  - Tool registration and routing                             │
│  - Request/response handling                                 │
│  - Error management                                          │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌───────▼────────┐
│   Formatters   │   │   WatsonxClient│
│  (lib/formatters)  │   (watsonx_client)│
│  - Response fmt │   │  - Token mgmt  │
│  - Test output  │   │  - API calls   │
│  - Visualizer   │   │  - Retry logic │
└────────────────┘   └───────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│   QA Sentry    │  │   AutoDocs     │  │  Visualizer    │
│ (lib/qa_sentry)│  │ (lib/autodocs) │  │(lib/visualizer)│
│  - Code scan   │  │  - Doc gen     │  │  - Diagrams    │
│  - Test gen    │  │  - API docs    │  │  - Analysis    │
│  - Auto-fix    │  │  - Guides      │  │  - Concepts    │
└────────────────┘  └────────────────┘  └───────┬────────┘
                                                 │
                                        ┌────────▼────────┐
                                        │   Renderers     │
                                        │(lib/visualizer/ │
                                        │   renderers.py) │
                                        │  - PNG gen      │
                                        │  - Kroki API    │
                                        └─────────────────┘
```

## Core Components

### 1. MCP Server (`server.py`)
**Responsibility:** Central orchestrator for all MCP tool operations

**Key Features:**
- Tool registration and routing
- Request validation
- Response formatting delegation
- Error handling and reporting

**Recent Improvements:**
- Extracted formatters to separate module
- Reduced from 532 lines to ~380 lines
- Improved maintainability and testability

### 2. WatsonxClient (`watsonx_client.py`)
**Responsibility:** IBM watsonx.ai API integration

**Key Features:**
- Token management with caching
- Text generation with configurable parameters
- PRD synthesis
- Retry logic with exponential backoff

**Critical Fixes:**
- ✅ **Token Refresh Race Condition** - Added `asyncio.Lock()` to prevent concurrent token refreshes
- ✅ **Retry Logic** - Implemented exponential backoff for network failures (1s, 2s, 4s delays)
- ✅ **Constants Usage** - Replaced magic numbers with named constants

**Architecture Decision:** 
- Uses async/await for non-blocking I/O
- Implements double-check locking pattern for optimal performance
- Retries on 5xx errors and 429 rate limits

### 3. Formatters Module (`lib/formatters.py`)
**Responsibility:** Response formatting for all tools

**Functions:**
- `format_test_generation_response()` - Unified formatter for network/unit tests
- `format_visualizer_result()` - Visualizer output formatting
- Helper functions for type-specific sections

**Design Decision:**
- Extracted from server.py to follow Single Responsibility Principle
- Eliminates 90% code duplication between test formatters
- Pure functions for easy testing

### 4. Renderers Module (`lib/visualizer/renderers.py`)
**Responsibility:** Diagram rendering and image generation

**Functions:**
- `save_mermaid_as_png()` - Converts Mermaid diagrams to PNG via Kroki API
- `DiagramGenerationError` - Custom exception for rendering failures

**Critical Fixes:**
- ✅ **Error Handling** - Raises exceptions instead of returning error strings
- ✅ **Validation** - Checks for empty mermaid code
- ✅ **Network Errors** - Wraps all errors in `DiagramGenerationError`

**Architecture Decision:**
- Separated from core visualization logic
- Uses Kroki API (no local dependencies)
- Proper exception hierarchy for error handling

### 5. Constants Module (`lib/utils/constants.py`)
**Responsibility:** Centralized configuration values

**Categories:**
- HTTP & Network (timeouts, retries)
- Token & Authentication (expiry, buffers)
- AI Model Parameters (tokens, temperature)
- Code Analysis & Chunking (sizes, overlaps)
- Cache Configuration (TTL, key lengths)
- File Processing (sizes, encodings, extensions)
- Visualization (depths, compression)
- QA Sentry (severity levels, scan types)

**Design Decision:**
- Single source of truth for all configuration
- Eliminates magic numbers throughout codebase
- Easy to modify and test

### 6. Cache System (`lib/utils/cache.py`)
**Responsibility:** File-based caching with memory layer

**Key Features:**
- MD5-based file hashing
- Memory cache for fast repeated access
- TTL-based expiration
- Operation-specific cache keys

**Critical Fixes:**
- ✅ **Cache Key Collision** - Includes file path hash in key generation
- Format: `operation_pathhash_contenthash`
- Prevents collisions when files have identical content

**Architecture Decision:**
- Two-tier caching (memory + disk)
- Path-aware keys prevent false cache hits
- Configurable TTL per cache instance

## Design Patterns

### 1. Async/Await Pattern
**Used in:** WatsonxClient, all tool handlers
**Benefit:** Non-blocking I/O for better performance

### 2. Double-Check Locking
**Used in:** Token refresh in WatsonxClient
**Benefit:** Optimal performance with thread safety

### 3. Retry with Exponential Backoff
**Used in:** WatsonxClient.generate_text()
**Benefit:** Resilience against transient failures

### 4. Factory Pattern
**Used in:** Cache system (get_cache())
**Benefit:** Singleton cache instance management

### 5. Strategy Pattern
**Used in:** Formatters for different test types
**Benefit:** Flexible formatting without code duplication

## Error Handling Strategy

### Exception Hierarchy
```
Exception
├── ValueError (configuration errors)
├── RuntimeError (API/network errors)
└── DiagramGenerationError (rendering errors)
    ├── Network errors
    ├── Validation errors
    └── File system errors
```

### Error Propagation
1. **Low-level errors** - Caught and wrapped in domain-specific exceptions
2. **Mid-level errors** - Logged and re-raised with context
3. **Top-level errors** - Formatted as user-friendly responses

### Retry Strategy
- **Retryable:** 5xx errors, 429 rate limits, network timeouts
- **Non-retryable:** 4xx errors (except 429), validation errors
- **Backoff:** Exponential (1s, 2s, 4s)

## Performance Optimizations

### 1. Token Caching
- Tokens cached until 60s before expiry
- Prevents redundant authentication calls
- Thread-safe with async lock

### 2. Two-Tier Cache
- Memory cache for instant access
- Disk cache for persistence
- Automatic promotion to memory on access

### 3. Lazy Loading
- Modules loaded on-demand
- Reduces startup time
- Lower memory footprint

### 4. Async I/O
- Non-blocking API calls
- Concurrent request handling
- Better resource utilization

## Testing Strategy

### Test Coverage
- **Unit Tests:** Individual functions and methods
- **Integration Tests:** Component interactions
- **Async Tests:** Concurrent operations
- **Error Tests:** Exception handling

### Test Files
- `test_improvements.py` - Tests for all recent fixes
- `test_cache_system.py` - Comprehensive cache tests
- `test_watsonx.py` - API integration tests
- `test_qa_sentry.py` - QA Sentry functionality

### Key Test Scenarios
1. Token refresh race conditions
2. Retry logic with network failures
3. Cache key collision prevention
4. PNG generation error handling
5. Formatter output validation
6. Constants usage verification

## Security Considerations

### 1. Credential Management
- API keys stored in `.env` file
- Never logged or exposed in responses
- Validated at initialization

### 2. File Access
- `.bobignore` file for sensitive paths
- Path validation to prevent traversal
- Size limits on file processing

### 3. API Rate Limiting
- Retry logic respects 429 responses
- Exponential backoff prevents hammering
- Token caching reduces auth calls

## Scalability Considerations

### 1. Horizontal Scaling
- Stateless server design
- Shared cache directory possible
- No in-memory session state

### 2. Vertical Scaling
- Async I/O for high concurrency
- Memory-efficient caching
- Lazy module loading

### 3. Performance Monitoring
- Cache hit/miss statistics
- Token refresh frequency
- API call latency tracking

## Future Improvements

### Planned Enhancements
1. **Dependency Injection** - Improve testability
2. **Type Hints** - Add TypedDict for structured data
3. **Prompt Builder** - DRY prompt construction
4. **Module Exports** - Standardize `__init__.py` files
5. **Visualizer Split** - Separate analyzer modules

### Technical Debt
1. Some broad exception catching remains
2. read_file_safe() return type inconsistency
3. Large visualizer/core.py needs splitting

## Deployment

### Requirements
- Python 3.8+
- IBM watsonx.ai credentials
- Network access to Kroki API (for PNG generation)

### Environment Variables
```
IBM_API_KEY=your_api_key
PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### Installation
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
pytest tests/ -v
```

## Changelog

### Version 2.0 (May 2026)
- ✅ Fixed token refresh race condition
- ✅ Fixed PNG generation error handling
- ✅ Added retry logic with exponential backoff
- ✅ Fixed cache key collision
- ✅ Eliminated 90% code duplication in formatters
- ✅ Created constants module
- ✅ Split server.py into formatters module
- ✅ Moved PNG generation to renderers module
- ✅ Added comprehensive test suite (22 tests, all passing)

### Version 1.0 (Initial Release)
- QA Sentry code analysis
- AutoDocs documentation generation
- Ideation framework
- Visualizer engine
- Basic caching system

## Contributing

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings with examples
- Keep functions under 50 lines

### Testing
- Write tests for new features
- Maintain >80% code coverage
- Test error cases
- Use mocks for external dependencies

### Documentation
- Update ARCHITECTURE.md for design changes
- Add inline comments for complex logic
- Update README.md for user-facing changes

---

**Last Updated:** May 17, 2026  
**Maintainer:** Bob Development Team  
**License:** See LICENSE file

# Made with Bob