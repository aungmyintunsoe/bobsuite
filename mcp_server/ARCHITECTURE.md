# BobSuite MCP Architecture Documentation

## 📋 Overview

This document explains what each file does, how they work together, and the overall architecture of the BobSuite MCP server.

## 🗂️ File Structure & Responsibilities

### Core Files

#### `server.py` - MCP Server Entry Point
**Purpose:** Main entry point that implements the Model Context Protocol server

**What it does:**
- Creates and manages the MCP server instance
- Registers 3 tools that IBM Bob can use:
  1. `scan_code_quality` - Analyzes code for bugs/vulnerabilities
  2. `generate_documentation` - Creates documentation
  3. `read_dataset_file` - Reads files from dataset
- Routes tool calls to appropriate modules
- Handles async communication with IBM Bob via stdio

**Key Components:**
- `BobSuiteMCPServer` class - Main server orchestrator
- `_register_handlers()` - Registers MCP tool handlers
- `run()` - Starts the server and listens for requests

**Dependencies:**
- `mcp` library for protocol implementation
- `watsonx_client` for AI capabilities
- `lib/*` modules for business logic

---

#### `watsonx_client.py` - IBM watsonx.ai Integration
**Purpose:** Handles all communication with IBM watsonx.ai API

**What it does:**
- Manages API credentials and authentication
- Provides async methods to generate text using AI models
- Builds specialized prompts for code analysis and documentation
- Handles errors and retries

**Key Methods:**
- `__init__()` - Loads credentials from .env file
- `_initialize_client()` - Sets up IBM watsonx.ai API client
- `generate_text()` - Generic text generation with any prompt
- `analyze_code()` - Specialized code analysis
- `generate_documentation()` - Specialized documentation generation
- `_build_analysis_prompt()` - Creates prompts for code analysis
- `_build_documentation_prompt()` - Creates prompts for docs

**Model Used:**
- Default: `ibm/granite-4-h-small
- Configurable via parameter

**Environment Variables Required:**
```
IBM_API_KEY=your_api_key_here
PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

### Business Logic Modules (`lib/`)

#### `lib/qa_sentry.py` - Code Quality Analysis
**Purpose:** Scans code for bugs, vulnerabilities, and quality issues

**What it does:**
- Reads code files from disk
- Detects programming language from file extension
- Uses watsonx.ai to analyze code for:
  - Bugs and errors
  - Security vulnerabilities
  - Code quality issues
  - Best practice violations
- Generates structured reports
- Supports batch scanning of multiple files

**Key Methods:**
- `scan_code()` - Main scanning function
- `_detect_language()` - Auto-detect programming language
- `_structure_results()` - Format analysis results
- `_generate_summary()` - Create issue summary
- `batch_scan()` - Scan multiple files
- `generate_report()` - Create markdown reports

**Supported Languages:**
Python, JavaScript, TypeScript, Java, C++, C, Go, Rust, Ruby, PHP, C#, Swift, Kotlin

---

#### `lib/doc_engine.py` - Documentation Generator
**Purpose:** Automatically generates comprehensive documentation for code

**What it does:**
- Reads code files
- Uses watsonx.ai to generate different types of documentation:
  - Inline comments and docstrings
  - API reference documentation
  - README sections
  - Full comprehensive docs
- Formats output with metadata
- Can document entire projects

**Key Methods:**
- `generate_docs()` - Main documentation generation
- `_detect_language()` - Identify programming language
- `_format_documentation()` - Add headers and metadata
- `generate_project_docs()` - Document entire codebase
- `generate_api_reference()` - Create API docs
- `generate_readme()` - Generate README files

**Documentation Types:**
- `inline` - Add comments to code
- `api` - API reference
- `readme` - README sections
- `full` - Comprehensive documentation

---

#### `lib/file_manager.py` - File Operations
**Purpose:** Manages file reading and operations for the dataset

**What it does:**
- Reads files from `dataset_balancia/` directory
- Provides file search and indexing
- Generates file statistics
- Formats file content with metadata
- Supports text-based file formats

**Key Methods:**
- `read_dataset_file()` - Read and format a file
- `list_dataset_files()` - List files with glob patterns
- `get_dataset_structure()` - Analyze directory structure
- `search_in_dataset()` - Search for text in files
- `get_file_stats()` - Get file statistics
- `create_file_index()` - Index files by extension

**Supported File Types:**
Source code, markup, config files, documentation (30+ extensions)

---

### Supporting Files

#### `requirements.txt` - Python Dependencies
Lists all required Python packages:
- `python-dotenv` - Environment variable management
- `mcp` - Model Context Protocol implementation
- `requests` - HTTP library


#### `test_watsonx.py` - Test Suite
Comprehensive test script to verify:
- Credentials are correct
- Connection to watsonx.ai works
- Text generation functions
- Code analysis works
- Documentation generation works
- Which models are available

**Usage:**
```bash
cd mcp_server
python test_watsonx.py
```

---

## 🔄 Data Flow

```
IBM Bob IDE
    ↓
[MCP Protocol via stdio]
    ↓
server.py (receives tool call)
    ↓
Routes to appropriate module:
    ├─→ qa_sentry.py (for code scanning)
    ├─→ doc_engine.py (for documentation)
    └─→ file_manager.py (for file reading)
         ↓
    Uses watsonx_client.py
         ↓
    IBM watsonx.ai API
         ↓
    Returns results to IBM Bob
```

## 🤖 Model Information

### Current Model: IBM Granite-4-h-small

**For IBM Bob Hackathon:**
The Granite models are IBM's own models and should be available in your watsonx.ai project. They're specifically designed for enterprise use cases including code analysis.

---

## 🔧 Error Types Explained

### Import Errors (in IDE)
The red squiggly lines you see are because:
1. **MCP library** - Not yet installed (`pip install mcp`)
2. **IBM watsonx.ai** - Not yet installed (`pip install ibm-watsonx-ai`)
3. **python-dotenv** - Not yet installed (`pip install python-dotenv`)

These are **expected** until you install the dependencies. The code will work once installed.

### Type Errors (Fixed)
- **doc_engine.py** - Fixed: Language parameter can now handle None values properly

---

## 📦 Suggested File Structure Improvements

### Current Structure (Good for Hackathon)
```
mcp_server/
├── server.py              # 139 lines - manageable
├── watsonx_client.py      # 176 lines - manageable
└── lib/
    ├── qa_sentry.py       # 221 lines - good
    ├── doc_engine.py      # 263 lines - good
    └── file_manager.py    # 260 lines - good
```

### If You Want to Split Further (Optional)

#### Option 1: Split by Concerns
```
mcp_server/
├── server.py
├── config/
│   ├── __init__.py
│   └── settings.py        # Environment & config
├── clients/
│   ├── __init__.py
│   └── watsonx_client.py
├── tools/
│   ├── __init__.py
│   ├── qa_sentry.py
│   ├── doc_engine.py
│   └── file_manager.py
└── utils/
    ├── __init__.py
    ├── prompts.py         # Prompt templates
    └── formatters.py      # Output formatting
```

#### Option 2: Split watsonx_client.py
```
clients/
├── __init__.py
├── base_client.py         # Connection & auth
├── text_generator.py      # Text generation
├── code_analyzer.py       # Code analysis
└── doc_generator.py       # Documentation
```

### Recommendation
**Keep current structure for hackathon** - it's clean, readable, and easy to understand. The files are well-sized and logically organized. Only split if:
1. Files exceed 500 lines
2. You're adding many more features
3. Multiple people are working on it

---

## 🧪 Testing Your Setup

### Step 1: Install Dependencies
```bash
cd mcp_server
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Step 3: Run Test
```bash
python test_watsonx.py
```

This will verify:
- ✓ Credentials are valid
- ✓ Connection works
- ✓ Text generation works
- ✓ Code analysis works
- ✓ Documentation generation works

### Step 4: Test with IBM Bob
Add to Bob's MCP settings and try:
```
Bob, use scan_code_quality to analyze dataset_balancia/example.py
```

---

## 📝 Summary

**Each file has a clear purpose:**
1. **server.py** - MCP protocol handler (the interface)
2. **watsonx_client.py** - AI communication (the brain)
3. **qa_sentry.py** - Code analysis (the inspector)
4. **doc_engine.py** - Documentation (the writer)
5. **file_manager.py** - File operations (the librarian)

**They work together like this:**
Bob → Server → Module → Watsonx Client → IBM AI → Results → Bob

The structure is clean, maintainable, and ready for the hackathon! 🚀