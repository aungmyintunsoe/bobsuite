# Bob Suite MCP Server - Comprehensive Documentation

**Generated:** 2026-05-17  
**Version:** 1.0  
**Project:** Bob Suite MCP Server

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Documentation Structure](#documentation-structure)
3. [Core Modules](#core-modules)
4. [Utility Modules](#utility-modules)
5. [Quick Navigation](#quick-navigation)
6. [Getting Started](#getting-started)
7. [Architecture Overview](#architecture-overview)
8. [Contributing](#contributing)

---

## Overview

This documentation repository contains comprehensive technical documentation for the **Bob Suite MCP Server** - an AI-powered development toolkit that provides advanced code analysis, documentation generation, ideation support, and visualization capabilities.

The Bob Suite MCP Server is built on the Model Context Protocol (MCP) and integrates with IBM's WatsonX AI platform to deliver intelligent development assistance.

### Key Features

- 🔍 **QA Sentry**: Multi-agent AI code scanner with debate pattern for comprehensive code analysis
- 📝 **AutoDocs**: Automated documentation generator supporting 12 documentation types
- 💡 **Ideation Engine**: AI-driven Technical Product Manager for PRD synthesis
- 📊 **Visualizer**: Project onboarding visualization generator (dependency chains, feature flows, concept maps)
- ⚡ **Performance Optimized**: File hash-based caching for 2-3x speedup
- 🔧 **Utility Suite**: Comprehensive utilities for logging, caching, file I/O, and formatting

---

## Documentation Structure

All documentation follows a consistent structure with the following sections:

1. **API Documentation** - Detailed API reference with parameters, return values, and usage examples
2. **Quick Start Guide** - Minimal setup steps and basic usage examples
3. **User Manual** - Comprehensive guide covering installation, configuration, and common use cases
4. **How-To Guide** - Step-by-step instructions for specific tasks
5. **Tutorial** - Interactive learning path with exercises and practice examples
6. **Troubleshooting Guide** - Common errors, debugging steps, FAQ, and known issues
7. **Requirements Specification** - Functional and non-functional requirements, dependencies, and acceptance criteria

---

## Core Modules

### 1. MCP Server Core
**File:** [`server-py-documentation.md`](server-py-documentation.md)

The main MCP server implementation that provides the foundation for all Bob Suite tools.

**Key Components:**
- MCP protocol implementation
- Tool registration and management
- Request/response handling
- Integration with WatsonX AI

**Status:** ⚠️ Documentation pending completion

---

### 2. QA Sentry
**File:** [`qa-sentry-core-documentation.md`](qa-sentry-core-documentation.md)

Multi-agent AI code scanner using a debate pattern between Finder and Critic agents.

**Key Features:**
- Multi-agent debate pattern for thorough analysis
- Supports bugs, vulnerabilities, quality, and comprehensive scans
- Auto-fix capabilities for identified issues
- Git diff scanning for changed lines only
- Unit test generation following Steve Sanderson principles
- Network performance test generation

**Main Methods:**
- `scan_code()` - Analyze code for bugs, vulnerabilities, and quality issues
- `batch_scan()` - Scan multiple files efficiently
- `scan_git_diff()` - Scan only changed lines from git diff
- `generate_unit_tests()` - Generate unit tests with S/S/R naming
- `generate_network_tests()` - Generate network performance tests

**Documentation Size:** 756 lines

---

### 3. AutoDocs
**File:** `autodocs-core-documentation.md` (pending)

Automated documentation generator supporting 12 different documentation types.

**Supported Documentation Types:**
1. User Manual
2. How-To Guide
3. Quick Start
4. Tutorial
5. Troubleshooting
6. User Persona
7. Knowledge Base
8. UX Design
9. Wireframe
10. Requirements
11. API Documentation
12. Full Documentation (all types combined)

**Main Methods:**
- `generate_docs()` - Generate documentation for code files
- `get_framework()` - Retrieve documentation framework
- `format_framework_for_display()` - Format framework for display

---

### 4. Ideation Engine
**File:** [`ideation-core-documentation.md`](ideation-core-documentation.md)

AI-driven Technical Product Manager for PRD synthesis using a 7-pillar ideation framework.

**7-Pillar Framework:**
1. **Problem Statement** - What problem are we solving?
2. **Target Users** - Who are we building for?
3. **Core Features** - What are the key capabilities?
4. **Success Metrics** - How do we measure success?
5. **Technical Considerations** - What are the technical constraints?
6. **Timeline & Milestones** - What's the delivery plan?
7. **Risks & Mitigation** - What could go wrong?

**Main Methods:**
- `get_framework()` - Retrieve the 7-pillar ideation framework
- `synthesize_prd()` - Generate PRD from conversation data
- `format_framework_for_display()` - Format framework for display

**Documentation Size:** 656 lines

---

### 5. Visualizer Engine
**File:** [`visualizer-core-documentation.md`](visualizer-core-documentation.md)

Project onboarding visualization generator using Mermaid diagrams.

**Visualization Types:**
1. **Dependency Chain** - Visual dependency mapping with configurable depth
2. **Feature Flow** - User journey and feature interaction mapping
3. **Project Concept** - High-level project architecture overview

**Main Methods:**
- `generate_dependency_chain()` - Generate dependency chain diagram
- `generate_feature_flow()` - Generate feature flow diagram
- `generate_project_concept()` - Generate project concept map

**Output Formats:**
- Mermaid diagram syntax
- PNG images via Kroki API
- SVG images via Kroki API

**Documentation Size:** 656 lines

---

## Utility Modules

### 1. Cache System
**File:** [`cache-py-documentation.md`](cache-py-documentation.md)

File-based caching system using MD5 hashing for performance optimization.

**Key Features:**
- File content hash-based cache keys
- Memory and disk caching
- Configurable TTL (Time-To-Live)
- 2-3x speedup for unchanged files

**Main Methods:**
- `get_file_hash()` - Generate MD5 hash of file content
- `get_cache_key()` - Generate unique cache key
- `get()` - Retrieve cached result
- `set()` - Store result in cache
- `clear()` - Clear cache entries
- `get_stats()` - Get cache statistics

**Documentation Size:** 456 lines

---

### 2. Logging System
**File:** [`logging-py-documentation.md`](logging-py-documentation.md)

MCP-specific logging utility that writes to stderr to avoid interfering with stdio communication.

**Key Features:**
- Writes to stderr (not stdout) for MCP compatibility
- Multiple log levels (debug, info, warning, error, critical)
- Optional file logging
- Global logger instance
- Convenience functions for quick logging

**Main Methods:**
- `get_logger()` - Get or create global logger instance
- `debug()`, `info()`, `warning()`, `error()`, `critical()` - Log at different levels
- `exception()` - Log exception with traceback

**Documentation Size:** 398 lines

---

### 3. File I/O
**File:** [`file-io-py-documentation.md`](file-io-py-documentation.md)

Safe file reading and language detection utilities.

**Key Features:**
- Safe file reading with exception handling
- Language detection based on file extensions
- Support for 40+ programming languages
- UTF-8 encoding with error handling

**Main Methods:**
- `detect_language()` - Detect programming language from file extension
- `read_file_safe()` - Safely read file content with error handling

**Supported Languages:** Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, R, Shell, SQL, HTML, CSS, and more.

**Documentation Size:** 329 lines

---

### 4. Formatting Utilities
**File:** [`formatting-py-documentation.md`](formatting-py-documentation.md)

Timestamp and markdown formatting utilities.

**Key Features:**
- ISO 8601 timestamp generation
- Markdown header formatting
- Metadata formatting with capitalization

**Main Methods:**
- `get_timestamp()` - Get current UTC timestamp in ISO format
- `format_markdown_header()` - Format markdown header with metadata

**Documentation Size:** 329 lines

---

### 5. Constants
**File:** [`constants-py-documentation.md`](constants-py-documentation.md)

Centralized configuration values to eliminate magic numbers.

**Configuration Categories:**
- HTTP & Network Configuration
- Token & Authentication
- AI Model Parameters
- Code Analysis & Chunking
- Cache Configuration
- File Processing
- Visualization
- QA Sentry
- HTTP Status Codes

**Key Constants:**
- `HTTP_TIMEOUT_SECONDS` - 60.0
- `DEFAULT_MAX_TOKENS` - 2000
- `CODE_ANALYSIS_TEMPERATURE` - 0.1
- `MAX_CHUNK_SIZE_LINES` - 1000
- `DEFAULT_CACHE_TTL_SECONDS` - 3600
- `MAX_FILE_SIZE_BYTES` - 10MB
- `SUPPORTED_EXTENSIONS` - 40+ file types

**Documentation Size:** 385 lines

---

## Quick Navigation

### By Module Type

**Core Functionality:**
- [QA Sentry](qa-sentry-core-documentation.md) - Code analysis and scanning
- [AutoDocs](autodocs-core-documentation.md) - Documentation generation (pending)
- [Ideation Engine](ideation-core-documentation.md) - PRD synthesis
- [Visualizer](visualizer-core-documentation.md) - Project visualization

**Utilities:**
- [Cache System](cache-py-documentation.md) - Performance optimization
- [Logging](logging-py-documentation.md) - MCP-compatible logging
- [File I/O](file-io-py-documentation.md) - Safe file operations
- [Formatting](formatting-py-documentation.md) - Timestamp and markdown utilities
- [Constants](constants-py-documentation.md) - Configuration values

### By Use Case

**Code Quality & Analysis:**
- [QA Sentry](qa-sentry-core-documentation.md) - Multi-agent code scanning
- [Constants](constants-py-documentation.md) - QA severity levels and scan types

**Documentation:**
- [AutoDocs](autodocs-core-documentation.md) - Automated documentation generation
- [Formatting](formatting-py-documentation.md) - Markdown formatting utilities

**Project Planning:**
- [Ideation Engine](ideation-core-documentation.md) - PRD synthesis and planning
- [Visualizer](visualizer-core-documentation.md) - Project visualization

**Performance & Infrastructure:**
- [Cache System](cache-py-documentation.md) - Caching for performance
- [Logging](logging-py-documentation.md) - Structured logging
- [File I/O](file-io-py-documentation.md) - Safe file operations

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- IBM WatsonX API credentials
- Git (for diff scanning features)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp_server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your WatsonX credentials
```

4. Run the MCP server:
```bash
python server.py
```

### Quick Start Examples

**Scan Code for Issues:**
```python
from lib.qa_sentry import scan_code

result = scan_code(
    file_path="example.py",
    scan_type="all",
    auto_fix=False
)
```

**Generate Documentation:**
```python
from lib.autodocs import generate_docs

result = generate_docs(
    file_path="example.py",
    doc_type="full"
)
```

**Create Project Visualization:**
```python
from lib.visualizer import generate_dependency_chain

result = generate_dependency_chain(
    project_path="./my_project",
    output_path="./docs/dependencies.png",
    max_depth=3
)
```

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Server Core                          │
│                    (server.py)                               │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  QA Sentry   │    │   AutoDocs   │    │  Ideation    │
│              │    │              │    │   Engine     │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                ┌──────────────────────┐
                │   WatsonX AI Client  │
                └──────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    Cache     │    │   Logging    │    │   File I/O   │
│   System     │    │   System     │    │   Utilities  │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Key Design Patterns

1. **Multi-Agent Debate Pattern** (QA Sentry)
   - Finder Agent: Identifies potential issues
   - Critic Agent: Validates and challenges findings
   - Consensus: Only confirmed issues are reported

2. **7-Pillar Framework** (Ideation Engine)
   - Structured approach to PRD synthesis
   - Ensures comprehensive coverage of all aspects

3. **File Hash-Based Caching** (Cache System)
   - MD5 hashing for content identification
   - Memory + Disk caching for optimal performance

4. **MCP Protocol Integration**
   - Stderr logging to avoid stdio interference
   - Async/await for non-blocking operations
   - Structured tool registration

---

## Contributing

### Documentation Standards

When contributing to this documentation:

1. **Follow the Structure**: Use the 7-section format (API, Quick Start, User Manual, How-To, Tutorial, Troubleshooting, Requirements)
2. **Be Comprehensive**: Include all methods, parameters, and return values
3. **Provide Examples**: Real-world usage examples are essential
4. **Keep Updated**: Update documentation when code changes
5. **Use Markdown**: Follow markdown best practices for formatting

### Generating Documentation

To generate documentation for a new module:

```python
from lib.autodocs import generate_docs

result = generate_docs(
    file_path="path/to/module.py",
    doc_type="full"
)
```

### Documentation Checklist

- [ ] API documentation with all methods
- [ ] Quick start guide with minimal example
- [ ] User manual with installation and configuration
- [ ] How-to guide with step-by-step instructions
- [ ] Tutorial with learning objectives and exercises
- [ ] Troubleshooting guide with common errors
- [ ] Requirements specification
- [ ] Code examples tested and verified
- [ ] Links to related documentation

---

## Additional Resources

### External Documentation

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [IBM WatsonX Documentation](https://www.ibm.com/watsonx)
- [Python Documentation](https://docs.python.org/)
- [Mermaid Diagram Syntax](https://mermaid.js.org/)
- [Kroki API](https://kroki.io/)

### Project Files

- `ARCHITECTURE.md` - Detailed architecture documentation
- `QUICKSTART.md` - Quick start guide for the project
- `README.md` - Main project README
- `INSTALL_DEPENDENCIES.md` - Dependency installation guide
- `requirements.txt` - Python dependencies

---

## Documentation Statistics

| Module | File | Lines | Status |
|--------|------|-------|--------|
| MCP Server Core | server-py-documentation.md | TBD | ⚠️ Pending |
| QA Sentry | qa-sentry-core-documentation.md | 756 | ✅ Complete |
| AutoDocs | autodocs-core-documentation.md | TBD | ⚠️ Pending |
| Ideation Engine | ideation-core-documentation.md | 656 | ✅ Complete |
| Visualizer | visualizer-core-documentation.md | 656 | ✅ Complete |
| Cache System | cache-py-documentation.md | 456 | ✅ Complete |
| Logging System | logging-py-documentation.md | 398 | ✅ Complete |
| File I/O | file-io-py-documentation.md | 329 | ✅ Complete |
| Formatting | formatting-py-documentation.md | 329 | ✅ Complete |
| Constants | constants-py-documentation.md | 385 | ✅ Complete |

**Total Documentation:** ~4,000+ lines across 10 modules

---

## License

Copyright © 2026 Bob Suite  
Licensed under the Apache License, Version 2.0

---

## Support

For questions, issues, or contributions:

- **GitHub Issues**: [Report an issue](https://github.com/your-repo/issues)
- **Documentation**: This README and linked documentation files
- **Community**: Join our discussion forums

---

**Last Updated:** 2026-05-17  
**Documentation Version:** 1.0  
**MCP Server Version:** Latest