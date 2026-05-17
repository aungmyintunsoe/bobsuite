# BobSuite MCP Architecture Documentation

## 📋 Overview

This document explains what each file does, how they work together, and the overall architecture of the BobSuite MCP server.

**Latest Update:** Added Ideation Engine - Feature Planning and PRD Generation (v2.0)

## 🗂️ File Structure & Responsibilities

### Core Files

#### `server.py` - MCP Server Entry Point
**Purpose:** Main entry point that implements the Model Context Protocol server

**What it does:**
- Creates and manages the MCP server instance
- Registers 5 tools that IBM Bob can use:
  1. `scan_code_quality` - Analyzes code for bugs/vulnerabilities
  2. `generate_documentation` - Creates documentation
  3. `scan_git_diff` - Scans git changes
  4. `get_project_framework` - Retrieves 7-pillar ideation framework
  5. `synthesize_project_plan` - Generates comprehensive PRDs
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
- `generate_text()` - Generic text generation with any prompt
- `synthesize_prd()` - Specialized PRD generation from conversation data
- `_build_ideation_prompt()` - Creates comprehensive prompts for PRD synthesis
- `_format_structured_conversation()` - Formats structured pillar data
- `_format_transcript_conversation()` - Formats raw conversation transcripts

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
#### `lib/ideation/core.py` - Ideation Engine
**Purpose:** Transforms IBM Bob into a proactive Technical Product Manager for feature planning

**What it does:**
- Provides a structured 7-pillar framework for feature planning:
  1. **Description** - What are we building?
  2. **In Scope** - What features are included?
  3. **Out of Scope** - What's explicitly excluded?
  4. **Implementation** - Technical approach and architecture
  5. **Acceptance Criteria** - How do we know it works?
  6. **Timeline** - Project phases and milestones
  7. **Resources** - Team, tools, and budget requirements
- Validates conversation data before PRD synthesis
- Orchestrates PRD generation using watsonx.ai
- Determines intelligent output paths for saving PRDs
- Formats framework for display in Bob's chat interface

**Key Methods:**
- `get_framework()` - Returns the 7-pillar structure
- `synthesize_prd()` - Main PRD generation orchestrator
- `_validate_input()` - Validates conversation completeness
- `_determine_output_path()` - AI-driven or user-specified file paths
- `_save_prd()` - Saves PRD to markdown file
- `format_framework_for_display()` - Creates readable framework guide

**Framework Philosophy:**
- AI-driven conversation flow (Bob decides when to ask follow-ups)
- Flexible data format (structured JSON or raw transcript)
- Dual output mode (chat display + file save)
- Quality validation (ensures critical pillars are answered)


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

### Code Quality & Documentation Flow
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

### Ideation Engine Flow (NEW)
```
Developer: "I want to plan a new feature"
    ↓
Bob calls get_project_framework
    ↓
IdeationEngine returns 7-pillar structure
    ↓
Bob conducts guided interview:
    - Asks pillar questions sequentially
    - AI decides when to ask follow-ups
    - Validates responses for completeness
    ↓
Developer completes all 7 pillars
    ↓
Bob calls synthesize_project_plan
    ↓
IdeationEngine validates conversation data
    ↓
watsonx_client.synthesize_prd()
    - Loads sample-prd.md as reference
    - Builds comprehensive synthesis prompt
    - Calls IBM Granite model
    ↓
AI generates professional PRD markdown
    ↓
IdeationEngine determines output path:
    - User-specified path (if provided)
    - AI-generated path based on project name
    - Default: ideation/{project}-prd-{timestamp}.md
    ↓
Save PRD to file + Return in chat
    ↓
Developer reviews PRD and starts coding
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

---

## 🧠 Ideation Engine - Feature Planning

### Overview
The Ideation Engine transforms IBM Bob from a reactive code-scanning tool into a proactive Technical Product Manager. It shifts AI integration to the very beginning of the SDLC—the planning phase.

### The 7-Pillar Framework

| Pillar | Question | Purpose | Importance |
|--------|----------|---------|------------|
| 1. Description | What are we building? | Define core objective, audience, and value | CRITICAL |
| 2. In Scope | What are we including? | Set MVP boundaries | CRITICAL |
| 3. Out of Scope | What are we excluding? | Prevent feature creep | HIGH |
| 4. Implementation | How might we build it? | Capture technical approach | MEDIUM |
| 5. Acceptance | How do we know it works? | Define success criteria | CRITICAL |
| 6. Timeline | What's the timeline? | Plan phases and milestones | CRITICAL |
| 7. Resources | What resources do we need? | Identify team, tools, budget | HIGH |

### Key Features

**AI-Driven Conversation**
- Bob manages the conversation flow dynamically
- Asks follow-up questions based on context
- Critiques responses to ensure quality
- No hardcoded validation rules

**Flexible Data Format**
- Accepts structured JSON (pillar-based)
- Accepts raw conversation transcripts
- Auto-detects format and adapts processing

**Intelligent Output**
- AI determines appropriate file path
- User can specify custom path
- Default: `ideation/{project-name}-prd-{timestamp}.md`
- Returns markdown in chat + saves to file

**Quality Validation**
- Ensures critical pillars are answered
- Checks minimum response lengths
- Validates completeness before synthesis
- Provides helpful error messages

### Usage Example

```python
# In IBM Bob chat:
Developer: "I want to plan a new feature"

Bob: "Great! Let's use the ideation framework. What are we building?"

Developer: "A real-time collaborative whiteboard for design teams"

Bob: "Interesting! Who is the target audience?"
# ... Bob continues through all 7 pillars with follow-ups

Bob: "Perfect! Let me synthesize this into a PRD..."
# Bob calls synthesize_project_plan internally

Bob: [Returns formatted PRD in chat]
"✅ PRD saved to: ideation/collaborative-whiteboard-prd-20260516.md"
```

### Testing

Run the comprehensive test suite:
```bash
cd mcp_server
python test_ideation.py
```

Tests include:
- Framework retrieval and structure validation
- Input validation (empty, incomplete, short responses)
- Output path determination logic
- PRD synthesis with structured data
- File saving functionality
- Display formatting

### Files

```
mcp_server/lib/ideation/
├── __init__.py              # Module exports
├── core.py                  # IdeationEngine class (428 lines)
├── sample-prd.md           # Reference template for AI
└── {generated-prds}.md     # Output files
```

---

## 🎨 Visualizer Engine - Project Onboarding

### Overview
The Visualizer Engine transforms complex codebases into visual diagrams, making it easy for new contributors to understand project structure, dependencies, and architecture at a glance.

### What it does:
- Analyzes project structure and generates three types of visualizations:
  1. **Dependency Chain** - Module relationships and imports
  2. **Feature Flow Maps** - User journeys and data flows
  3. **Project Concept Maps** - High-level architecture overview
- Outputs beautiful Mermaid diagrams embedded in markdown
- Uses AI to understand architecture and feature flows
- Perfect for onboarding, documentation, and code reviews

### Key Components:

**Dependency Chain Analyzer**
- Parses Python import statements using AST
- Builds module dependency graph
- Distinguishes internal vs external dependencies
- Generates Mermaid flowchart diagrams
- No AI required - fast and deterministic

**Feature Flow Mapper**
- Uses AI to analyze codebase and identify features
- Traces user journeys through the system
- Maps data flow between components
- Generates Mermaid sequence diagrams
- AI-powered for intelligent feature detection

**Project Concept Visualizer**
- Uses AI to understand high-level architecture
- Identifies main components (Server, Database, API, UI, etc.)
- Maps component relationships
- Detects external service integrations
- Generates Mermaid architecture diagrams

### Files

```
mcp_server/lib/visualizer/
├── __init__.py              # Module exports
├── core.py                  # VisualizerEngine class (783 lines)
├── USAGE_GUIDE.md          # Comprehensive usage documentation
└── {generated-diagrams}.md # Output visualization files
```

### Usage Example

```python
# In IBM Bob chat:
Developer: "Generate a dependency chain for the mcp_server directory"

Bob: [Analyzes imports and creates diagram]
"✅ Dependency chain generated!
- Total modules: 15
- Total dependencies: 42
- External deps: 8

[Displays Mermaid diagram showing module relationships]

✅ Saved to: visualizations/dependency-chain-2026-05-16.md"
```

### Testing

Run the comprehensive test suite:
```bash
cd mcp_server
python test_visualizer.py
```

Tests include:
- Dependency chain generation and validation
- Feature flow mapping with AI
- Project concept visualization
- Error handling with invalid inputs
- File saving functionality
- Mermaid diagram syntax validation

---

## 📝 Summary

**Each file has a clear purpose:**

1. **server.py** - MCP protocol handler (the interface)
2. **watsonx_client.py** - AI communication (the brain)
3. **qa_sentry.py** - Code analysis (the inspector)
4. **doc_engine.py** - Documentation (the writer)
5. **ideation_engine.py** - Feature planning (the product manager)
6. **visualizer.py** - Project visualization (the cartographer) 🆕

**They work together like this:**
Bob → Server → Module → Watsonx Client → IBM AI → Results → Bob

The structure is clean, maintainable, and ready for the hackathon! 🚀