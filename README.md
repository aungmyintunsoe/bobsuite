# BobSuite MCP - AI-Powered Code Analysis for IBM Bob

A Model Context Protocol (MCP) server that extends IBM Bob's capabilities with AI-powered code analysis and documentation tools, powered by IBM watsonx.ai.

## 🎯 Project Overview

BobSuite MCP is a tool suite that allows IBM Bob to:
- **Scan code for bugs and vulnerabilities** using watsonx.ai (QA Sentry)
- **Generate comprehensive documentation** automatically (Doc Engine)
- **Manage and analyze project files** intelligently (File Manager)

## 📁 Project Structure

```
bobsuite-monorepo/
├── .bobignore                 # Protects sensitive files from IBM Bob
├── .gitignore                 # Git ignore patterns
├── README.md                  # This file
│
├── mcp_server/                # THE CORE PRODUCT (Python)
│   ├── server.py              # MCP entry point
│   ├── watsonx_client.py      # IBM watsonx.ai API client
│   ├── .env.example           # Environment variables template
│   └── lib/                   # Business logic modules
│       ├── __init__.py
│       ├── qa_sentry.py       # Bug/vulnerability scanner
│       ├── doc_engine.py      # Documentation generator
│       └── file_manager.py    # File operations manager
│
├── landing_page/              # THE DEMO (HTML/CSS)
│   ├── index.html             # Landing page
│   └── style.css              # Styles
│
├── dataset_balancia/          # THE TEST SUBJECT
│   └── README.md              # (Your Balancia project goes here)
│
└── bob_sessions/              # THE JUDGING FOLDER
    └── README.md              # (Exported markdown reports)
```

## 🚀 Quick Start

**👉 See [QUICKSTART.md](QUICKSTART.md) for detailed step-by-step setup instructions!**

### TL;DR

```bash
# 1. Install dependencies
cd mcp_server
python -m venv venv
venv\Scripts\activate  # Windows for 
pip install -r requirements.txt

# 2. Configure credentials
cp .env
# Edit .env with your IBM_API_KEY and PROJECT_ID

# 3. Test connection
python test_watsonx.py

# 4. Configure IBM Bob MCP settings (see QUICKSTART.md)

# 5. Start using the tools in IBM Bob!
```

### Prerequisites

- Python 3.8+
- IBM Cloud account with watsonx.ai access
- IBM Bob IDE
- IBM API Key and Project ID

## 🛠️ Available Tools

### 1. **scan_code_quality**
Analyze code for bugs, vulnerabilities, and quality issues.

**Parameters:**
- `file_path` (required): Path to the code file
- `scan_type` (optional): "bugs", "vulnerabilities", "quality", or "all"

**Example:**
```
Use scan_code_quality on dataset_balancia/main.py with scan_type "all"
```

### 2. **generate_documentation**
Generate comprehensive documentation for code.

**Parameters:**
- `file_path` (required): Path to the code file
- `doc_type` (optional): "inline", "api", "readme", or "full"

**Example:**
```
Generate documentation for dataset_balancia/utils.py with doc_type "full"
```

### 3. **read_dataset_file**
Read and analyze files from the dataset_balancia directory.

**Parameters:**
- `file_path` (required): Relative path within dataset_balancia/

**Example:**
```
Read dataset_balancia/config.json
```

## 📊 Features

### QA Sentry
- **Bug Detection**: Identifies potential bugs and errors
- **Vulnerability Scanning**: Security analysis
- **Code Quality**: Best practices and improvements
- **Batch Scanning**: Analyze multiple files
- **Report Generation**: Markdown reports for judging

### Doc Engine
- **Inline Comments**: Add docstrings and comments
- **API Documentation**: Generate API references
- **README Generation**: Create project documentation
- **Usage Examples**: Generate code examples
- **Project-wide Docs**: Document entire codebases

### File Manager
- **Smart Reading**: Read and format code files
- **File Search**: Search across the dataset
- **Structure Analysis**: Understand project layout
- **Statistics**: File metrics and analysis
- **Index Creation**: Organize files by type

## 🎓 Usage Examples

### Example 1: Scan Code Quality
```
Bob, use the scan_code_quality tool to analyze dataset_balancia/app.py for all issues
```

### Example 2: Generate Documentation
```
Bob, generate full documentation for dataset_balancia/models.py
```

### Example 3: Read and Analyze
```
Bob, read dataset_balancia/README.md and summarize the project
```

## 🔧 Testing & Development

### Test Your Setup

**Run the comprehensive test suite:**
```bash
cd mcp_server
python test_watsonx.py
```

This will verify:
- ✓ Credentials are valid
- ✓ Connection to watsonx.ai works
- ✓ Text generation functions
- ✓ Code analysis works
- ✓ Documentation generation works
- ✓ Available models in your project

### Adding New Tools

1. Create a new module in `mcp_server/lib/`
2. Implement your tool logic using `WatsonxClient`
3. Register the tool in `server.py`:
   ```python
   Tool(
       name="your_tool_name",
       description="What it does",
       inputSchema={...}
   )
   ```
4. Add handler in `call_tool()` method
5. Update documentation

### Understanding the Architecture

See [mcp_server/ARCHITECTURE.md](mcp_server/ARCHITECTURE.md) for:
- Detailed explanation of each file
- Data flow diagrams
- Model information
- File structure recommendations

## 📝 Next Steps

1. **Set up your environment** with IBM credentials
2. **Add your Balancia project** to `dataset_balancia/`
3. **Test the MCP server** with IBM Bob
4. **Generate reports** and save to `bob_sessions/`
5. **Prepare demo** using the landing page

## 🏆 Hackathon Judging

All session outputs and demonstrations should be saved in `bob_sessions/` as markdown files for judging purposes.

## 🤝 Contributing

This is a hackathon project. Feel free to extend and improve!

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Links

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [IBM Bob IDE](https://www.ibm.com/products/ibm-bob)

---

**Built for IBM Bob Hackathon 2026** 🚀