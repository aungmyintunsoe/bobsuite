# 🚀 MCP Server Setup & Testing Guide

Complete guide for setting up and testing the BobSuite MCP server with IBM Bob.

## 📊 Current Status

✅ **MCP Server**: Fully implemented with 10 tools  
✅ **Credentials**: Configured in `.env` file  
🔄 **Next Steps**: Testing and IBM Bob integration

---

## 🧪 Phase 1: Local Testing (Before IBM Bob Integration)

### Step 1: Verify Python Environment

```bash
cd mcp_server
python --version  # Should be 3.8+
```

### Step 2: Install/Verify Dependencies

```bash
# Create virtual environment (if not exists)
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

**Expected packages:**
- `mcp>=0.9.0`
- `python-dotenv>=1.0.0`
- `httpx>=0.24.0`
- `pytest>=7.0.0`
- `gitpython>=3.1.0`

### Step 3: Test Watsonx Connection

Create a quick test script:

```bash
python -c "
from watsonx_client import WatsonxClient
import asyncio

async def test():
    client = WatsonxClient()
    print('✓ WatsonxClient initialized')
    print(f'  API Key: {client.api_key[:10]}...')
    print(f'  Project ID: {client.project_id}')
    print(f'  URL: {client.watsonx_url}')

asyncio.run(test())
"
```

**Expected output:**
```
✓ WatsonxClient initialized
  API Key: pak-xxxxx...
  Project ID: your-project-id
  URL: https://us-south.ml.cloud.ibm.com
```

### Step 4: Test MCP Server Startup

```bash
# Test if server starts without errors
python server.py
```

**Expected behavior:**
- Server should start and wait for input (stdio mode)
- No error messages
- Press Ctrl+C to stop

**Common issues:**
- ❌ `ModuleNotFoundError` → Run `pip install -r requirements.txt`
- ❌ `ValueError: Missing required environment variables` → Check `.env` file
- ❌ Import errors → Verify all files in `lib/` directory exist

---

## 🔌 Phase 2: IBM Bob MCP Configuration

### Step 1: Locate IBM Bob MCP Settings

IBM Bob MCP settings are typically in one of these locations:

**Windows:**
```
%APPDATA%\Code\User\globalStorage\ibm.bob\settings.json
```

**Mac/Linux:**
```
~/.config/Code/User/globalStorage/ibm.bob/settings.json
```

Or use IBM Bob's settings UI:
1. Open IBM Bob
2. Go to Settings (Ctrl+,)
3. Search for "MCP"
4. Click "Edit in settings.json"

### Step 2: Add BobSuite MCP Server

Add this configuration to your MCP settings:

```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["d:/bobsuite/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "d:/bobsuite/mcp_server"
      }
    }
  }
}
```

**⚠️ Important:** Replace `d:/bobsuite` with your actual project path!

**Alternative (if Python not in PATH):**
```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "C:/Python39/python.exe",
      "args": ["d:/bobsuite/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "d:/bobsuite/mcp_server"
      }
    }
  }
}
```

### Step 3: Restart IBM Bob

1. Close all IBM Bob windows
2. Restart IBM Bob
3. Check the Output panel for MCP server logs

**Expected logs:**
```
[MCP] Starting server: bobsuite
[MCP] Server bobsuite started successfully
[MCP] Discovered 10 tools from bobsuite
```

---

## 🧪 Phase 3: Testing Individual Tools

### Test Strategy

Test tools in order of complexity:
1. **Simple** → Core functionality
2. **Medium** → Advanced features
3. **Complex** → Full integration

### Test 1: scan_code_quality (Simple)

**Command in IBM Bob:**
```
Bob, use scan_code_quality to analyze mcp_server/server.py with scan_type "quality"
```

**Expected output:**
- Markdown report with code quality analysis
- Suggestions for improvements
- No errors

**What it tests:**
- ✓ MCP server communication
- ✓ Watsonx.ai connection
- ✓ File reading
- ✓ QASentry module

### Test 2: generate_documentation (Simple)

**Command in IBM Bob:**
```
Bob, generate documentation for mcp_server/watsonx_client.py with doc_type "api"
```

**Expected output:**
- API documentation in markdown
- Function descriptions
- Parameter details

**What it tests:**
- ✓ AutoDocs module
- ✓ Code parsing
- ✓ Documentation generation

### Test 3: generate_project_concept (Medium)

**Command in IBM Bob:**
```
Bob, generate a project concept map for the mcp_server directory
```

**Expected output:**
- Mermaid diagram showing architecture
- Component relationships
- High-level overview

**What it tests:**
- ✓ VisualizerEngine module
- ✓ Project analysis
- ✓ Diagram generation

### Test 4: generate_unit_tests (Complex)

**Command in IBM Bob:**
```
Bob, generate unit tests for mcp_server/watsonx_client.py
```

**Expected output:**
- Complete test file with pytest tests
- Steve Sanderson principles applied
- Mock implementations

**What it tests:**
- ✓ Test generation
- ✓ Code analysis
- ✓ Framework detection

### Test 5: scan_git_diff (Integration)

**Command in IBM Bob:**
```
Bob, use scan_git_diff to analyze changes in the current repository
```

**Expected output:**
- Analysis of git changes
- Quality assessment of modifications

**What it tests:**
- ✓ Git integration
- ✓ Diff parsing
- ✓ Change analysis

---

## 📋 Complete Tool Reference

### Core Analysis Tools

| Tool | Purpose | Test Priority |
|------|---------|---------------|
| `scan_code_quality` | Bug/vulnerability detection | 🔴 High |
| `generate_documentation` | Auto-generate docs | 🔴 High |
| `scan_git_diff` | Analyze git changes | 🟡 Medium |

### Visualization Tools

| Tool | Purpose | Test Priority |
|------|---------|---------------|
| `generate_dependency_chain` | Module relationships | 🟡 Medium |
| `generate_feature_flow` | User journey maps | 🟡 Medium |
| `generate_project_concept` | Architecture overview | 🟡 Medium |

### Planning Tools

| Tool | Purpose | Test Priority |
|------|---------|---------------|
| `get_project_framework` | 7-pillar ideation | 🟢 Low |
| `synthesize_project_plan` | PRD generation | 🟢 Low |

### Testing Tools

| Tool | Purpose | Test Priority |
|------|---------|---------------|
| `generate_unit_tests` | Unit test generation | 🟡 Medium |
| `generate_network_performance_tests` | API test generation | 🟢 Low |

---

## 🎯 Usage Examples for IBM Bob

### Example 1: Full Code Review

```
Bob, I need a comprehensive code review of mcp_server/lib/qa_sentry/core.py. 
Please:
1. Scan for bugs and vulnerabilities
2. Generate API documentation
3. Create unit tests
```

### Example 2: Project Onboarding

```
Bob, help me understand this project:
1. Generate a project concept map for mcp_server
2. Create a dependency chain diagram
3. Generate a feature flow for the QA Sentry module
```

### Example 3: Documentation Sprint

```
Bob, document the entire mcp_server/lib directory:
1. Generate API docs for each module
2. Create a comprehensive README
3. Add usage examples
```

### Example 4: Quality Assurance

```
Bob, perform QA on my recent changes:
1. Scan git diff for issues
2. Generate tests for modified files
3. Check code quality
```

---

## 🐛 Troubleshooting

### Issue: "Server failed to start"

**Symptoms:**
- IBM Bob shows error in Output panel
- No tools discovered

**Solutions:**
1. Check Python path in MCP settings
2. Verify `server.py` path is correct
3. Test server manually: `python mcp_server/server.py`
4. Check for syntax errors in `server.py`

### Issue: "Tool execution failed"

**Symptoms:**
- Tool is discovered but fails when called
- Error message in IBM Bob

**Solutions:**
1. Check `.env` file exists and has credentials
2. Verify watsonx.ai connection: `python -c "from watsonx_client import WatsonxClient; WatsonxClient()"`
3. Check file paths are relative to workspace
4. Review error message for specific issues

### Issue: "Invalid credentials"

**Symptoms:**
- Authentication errors
- 401/403 HTTP errors

**Solutions:**
1. Verify `IBM_API_KEY` in `.env`
2. Check `PROJECT_ID` is correct
3. Ensure API key has watsonx.ai access
4. Try regenerating API key in IBM Cloud

### Issue: "Module not found"

**Symptoms:**
- Import errors in logs
- Server fails to start

**Solutions:**
1. Activate virtual environment
2. Run `pip install -r requirements.txt`
3. Check `PYTHONPATH` in MCP settings
4. Verify all files in `lib/` exist

### Issue: "Slow responses"

**Symptoms:**
- Tools take long time to respond
- Timeouts

**Solutions:**
1. Check internet connection
2. Verify watsonx.ai service status
3. Reduce file size for analysis
4. Check `HTTP_TIMEOUT_SECONDS` in `lib/utils/constants.py`

---

## 📊 Testing Checklist

### Pre-Integration Testing
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists with credentials
- [ ] WatsonxClient initializes without errors
- [ ] `server.py` starts without errors

### IBM Bob Integration
- [ ] MCP settings configured with correct paths
- [ ] IBM Bob restarted
- [ ] Server appears in MCP servers list
- [ ] 10 tools discovered
- [ ] No errors in Output panel

### Tool Testing
- [ ] `scan_code_quality` works
- [ ] `generate_documentation` works
- [ ] `generate_project_concept` works
- [ ] `generate_dependency_chain` works
- [ ] `generate_unit_tests` works
- [ ] `scan_git_diff` works
- [ ] Error handling works properly
- [ ] Output formats are correct

### Production Readiness
- [ ] All tools tested successfully
- [ ] Documentation complete
- [ ] Usage examples created
- [ ] Troubleshooting guide reviewed
- [ ] Performance acceptable
- [ ] Error messages clear and helpful

---

## 🚀 Next Steps After Setup

1. **Test with Real Code**
   - Analyze your actual project files
   - Generate documentation for your codebase
   - Create visualizations

2. **Customize Prompts**
   - Adjust prompts in `lib/*/prompts.py` files
   - Tune for your specific needs
   - Test improvements

3. **Extend Functionality**
   - Add new tools to `server.py`
   - Create custom analysis modules
   - Integrate additional services

4. **Document Sessions**
   - Save analysis reports to `bob_sessions/`
   - Export visualizations
   - Create demo materials

---

## 📚 Additional Resources

- **Architecture Details**: See `mcp_server/reports/ARCHITECTURE.md`
- **Quick Start**: See `QUICKSTART.md`
- **Main README**: See `README.md`
- **MCP Protocol**: https://modelcontextprotocol.io/
- **IBM watsonx.ai**: https://www.ibm.com/docs/en/watsonx-as-a-service

---

**Ready to test?** Start with Phase 1 local testing, then move to IBM Bob integration! 🎯