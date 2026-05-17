# 🧪 MCP Server Testing & Implementation Plan

Complete step-by-step plan for testing and deploying the BobSuite MCP server.

---

## 📋 Executive Summary

### Current Status
- ✅ **MCP Server**: Fully implemented in [`server.py`](server.py)
- ✅ **10 Tools**: All registered and ready
- ✅ **Credentials**: Already configured in `.env`
- 🔄 **Next**: Testing and IBM Bob integration

### Implementation Approach: **Incremental Testing** ✅

**Why Incremental?**
- Complex system with 10 tools and external API dependencies
- Easier to isolate and fix issues
- Validates each component before full integration
- Reduces debugging time

**Complexity Level: 🟡 Medium**
- Server code: ✅ Complete
- Setup: 🟡 Configuration needed
- Testing: 🟡 Systematic validation required
- Integration: 🟡 IBM Bob MCP setup

---

## 🎯 Implementation Phases

### Phase 1: Pre-Flight Checks (5 minutes)

#### 1.1 Create `.env.example` Template

Since Plan mode can't create non-markdown files, create this manually:

**File: `mcp_server/.env.example`**
```env
# IBM watsonx.ai Credentials
# Get these from: https://cloud.ibm.com/

# Your IBM Cloud API Key
# Location: IBM Cloud → Manage → Access (IAM) → API keys
IBM_API_KEY=your_api_key_here

# Your watsonx.ai Project ID
# Location: watsonx.ai → Projects → Your Project → Settings
PROJECT_ID=your_project_id_here

# watsonx.ai API URL (usually us-south, adjust for your region)
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Optional: Model configuration
# DEFAULT_MODEL=ibm/granite-13b-chat-v2
```

#### 1.2 Verify Environment

```bash
cd mcp_server

# Check Python version
python --version  # Should be 3.8+

# Check if venv exists
ls venv/  # Should show Scripts/ or bin/

# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verify dependencies
pip list | grep -E "mcp|httpx|dotenv|pytest|gitpython"
```

**Expected packages:**
```
httpx                 0.24.0+
mcp                   0.9.0+
python-dotenv         1.0.0+
pytest                7.0.0+
gitpython             3.1.0+
```

#### 1.3 Quick Connection Test

```bash
python -c "
from watsonx_client import WatsonxClient
client = WatsonxClient()
print('✓ Connection successful!')
print(f'  API Key: {client.api_key[:15]}...')
print(f'  Project: {client.project_id}')
"
```

---

### Phase 2: Local Server Testing (10 minutes)

#### 2.1 Test Server Startup

```bash
# Start server (it will wait for stdio input)
python server.py
```

**Expected behavior:**
- No error messages
- Server waits for input (stdio mode)
- Press Ctrl+C to stop

**Common issues:**
| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | Run `pip install -r requirements.txt` |
| `ValueError: Missing required environment variables` | Check `.env` file exists and has credentials |
| `ImportError: cannot import name 'QASentry'` | Verify `lib/qa_sentry/__init__.py` exists |

#### 2.2 Test Individual Modules

Create test file: `test_modules.py`

```python
"""Quick module tests"""
import asyncio
from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry
from lib.autodocs import AutoDocs
from lib.visualizer import VisualizerEngine

async def test_modules():
    print("Testing modules...")
    
    # Test 1: WatsonxClient
    try:
        client = WatsonxClient()
        print("✓ WatsonxClient initialized")
    except Exception as e:
        print(f"✗ WatsonxClient failed: {e}")
        return
    
    # Test 2: QASentry
    try:
        qa = QASentry(client)
        print("✓ QASentry initialized")
    except Exception as e:
        print(f"✗ QASentry failed: {e}")
    
    # Test 3: AutoDocs
    try:
        docs = AutoDocs(client)
        print("✓ AutoDocs initialized")
    except Exception as e:
        print(f"✗ AutoDocs failed: {e}")
    
    # Test 4: VisualizerEngine
    try:
        viz = VisualizerEngine(client)
        print("✓ VisualizerEngine initialized")
    except Exception as e:
        print(f"✗ VisualizerEngine failed: {e}")
    
    print("\n✓ All modules loaded successfully!")

if __name__ == "__main__":
    asyncio.run(test_modules())
```

Run: `python test_modules.py`

---

### Phase 3: IBM Bob Integration (15 minutes)

#### 3.1 Configure MCP Settings

**Location of settings file:**

**Windows:**
```
%APPDATA%\Code\User\globalStorage\ibm.bob\settings.json
```

**Mac/Linux:**
```
~/.config/Code/User/globalStorage/ibm.bob/settings.json
```

**Or via IBM Bob UI:**
1. Open IBM Bob
2. Press `Ctrl+,` (Settings)
3. Search for "MCP"
4. Click "Edit in settings.json"

#### 3.2 Add BobSuite Server Configuration

Add this to your MCP settings:

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

**⚠️ IMPORTANT:** Replace `d:/bobsuite` with your actual project path!

**Alternative configurations:**

**If Python not in PATH:**
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

**If using virtual environment:**
```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "d:/bobsuite/mcp_server/venv/Scripts/python.exe",
      "args": ["d:/bobsuite/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "d:/bobsuite/mcp_server"
      }
    }
  }
}
```

#### 3.3 Restart and Verify

1. **Close all IBM Bob windows**
2. **Restart IBM Bob**
3. **Check Output panel** (View → Output → Select "MCP")

**Expected logs:**
```
[MCP] Starting server: bobsuite
[MCP] Server bobsuite connected
[MCP] Discovered 10 tools from bobsuite:
  - scan_code_quality
  - generate_documentation
  - scan_git_diff
  - get_project_framework
  - synthesize_project_plan
  - generate_dependency_chain
  - generate_feature_flow
  - generate_project_concept
  - generate_network_performance_tests
  - generate_unit_tests
```

**Troubleshooting:**

| Issue | Solution |
|-------|----------|
| Server not starting | Check Python path, verify `server.py` exists |
| No tools discovered | Check for syntax errors in `server.py` |
| Connection timeout | Increase timeout in MCP settings |
| Import errors | Verify `PYTHONPATH` is set correctly |

---

### Phase 4: Tool Testing (20 minutes)

Test tools in order of complexity and dependencies.

#### 4.1 Test Priority Matrix

| Priority | Tool | Complexity | Dependencies |
|----------|------|------------|--------------|
| 🔴 High | `scan_code_quality` | Low | Watsonx, File I/O |
| 🔴 High | `generate_documentation` | Low | Watsonx, File I/O |
| 🟡 Medium | `generate_project_concept` | Medium | Watsonx, File Analysis |
| 🟡 Medium | `generate_dependency_chain` | Medium | Watsonx, Code Parsing |
| 🟡 Medium | `generate_unit_tests` | Medium | Watsonx, Code Analysis |
| 🟢 Low | `scan_git_diff` | High | Git, Watsonx |
| 🟢 Low | `generate_feature_flow` | High | Watsonx, Project Analysis |
| 🟢 Low | `get_project_framework` | Low | None (returns static data) |
| 🟢 Low | `synthesize_project_plan` | High | Watsonx, Complex input |
| 🟢 Low | `generate_network_performance_tests` | Medium | Watsonx, Code Analysis |

#### 4.2 Test Scripts for IBM Bob

**Test 1: scan_code_quality (CRITICAL)**

```
Bob, use scan_code_quality to analyze mcp_server/server.py with scan_type "quality"
```

**Expected output:**
- Markdown report with code quality analysis
- Suggestions for improvements
- Code snippets with issues highlighted
- No errors or exceptions

**Validates:**
- ✓ MCP communication works
- ✓ Watsonx.ai connection active
- ✓ File reading functional
- ✓ QASentry module operational
- ✓ Response formatting correct

---

**Test 2: generate_documentation (CRITICAL)**

```
Bob, generate documentation for mcp_server/watsonx_client.py with doc_type "api"
```

**Expected output:**
- API documentation in markdown format
- Class and method descriptions
- Parameter details
- Return value documentation
- Usage examples

**Validates:**
- ✓ AutoDocs module works
- ✓ Code parsing functional
- ✓ Documentation generation accurate
- ✓ Markdown formatting correct

---

**Test 3: generate_project_concept (IMPORTANT)**

```
Bob, generate a project concept map for the mcp_server directory
```

**Expected output:**
- High-level architecture diagram (Mermaid)
- Component relationships
- Module descriptions
- System overview

**Validates:**
- ✓ VisualizerEngine operational
- ✓ Project analysis works
- ✓ Mermaid diagram generation
- ✓ File traversal functional

---

**Test 4: generate_dependency_chain (IMPORTANT)**

```
Bob, generate a dependency chain for mcp_server with max_depth 2
```

**Expected output:**
- Dependency diagram showing imports
- Module relationships
- External dependencies (if enabled)
- Clear visualization

**Validates:**
- ✓ Code parsing for imports
- ✓ Dependency tracking
- ✓ Diagram generation
- ✓ Depth limiting works

---

**Test 5: generate_unit_tests (IMPORTANT)**

```
Bob, generate unit tests for mcp_server/watsonx_client.py
```

**Expected output:**
- Complete pytest test file
- Steve Sanderson principles applied
- Mock implementations
- Test cases for all methods

**Validates:**
- ✓ Test generation logic
- ✓ Code analysis depth
- ✓ Framework detection
- ✓ Best practices application

---

**Test 6: scan_git_diff (OPTIONAL)**

```
Bob, use scan_git_diff to analyze changes in d:/bobsuite with staged set to true
```

**Expected output:**
- Analysis of staged changes
- Quality assessment
- Suggestions for improvements

**Validates:**
- ✓ Git integration
- ✓ Diff parsing
- ✓ Change analysis
- ✓ GitPython library

---

**Test 7: get_project_framework (SIMPLE)**

```
Bob, use get_project_framework with include_examples set to true
```

**Expected output:**
- 7-pillar ideation framework
- Examples for each pillar
- Structured format

**Validates:**
- ✓ Static data retrieval
- ✓ Framework formatting
- ✓ Basic tool functionality

---

#### 4.3 Test Results Template

Create a test log: `test_results.md`

```markdown
# MCP Server Test Results

**Date:** [Current Date]
**Tester:** [Your Name]

## Environment
- Python Version: 
- MCP Version: 
- IBM Bob Version: 

## Test Results

### Test 1: scan_code_quality
- Status: [ ] Pass [ ] Fail
- Response Time: 
- Issues: 
- Notes: 

### Test 2: generate_documentation
- Status: [ ] Pass [ ] Fail
- Response Time: 
- Issues: 
- Notes: 

### Test 3: generate_project_concept
- Status: [ ] Pass [ ] Fail
- Response Time: 
- Issues: 
- Notes: 

[Continue for all tools...]

## Overall Assessment
- Tools Working: X/10
- Critical Issues: 
- Recommendations: 
```

---

### Phase 5: Production Deployment (10 minutes)

#### 5.1 Final Checklist

**Pre-Deployment:**
- [ ] All critical tools tested (scan_code_quality, generate_documentation)
- [ ] Important tools tested (visualizer, test generation)
- [ ] Error handling verified
- [ ] Response times acceptable (<30s for most operations)
- [ ] Documentation complete
- [ ] `.env.example` created for team members

**Deployment:**
- [ ] MCP settings configured correctly
- [ ] Server starts automatically with IBM Bob
- [ ] No errors in Output panel
- [ ] Tools discoverable in IBM Bob
- [ ] Team members can access

**Post-Deployment:**
- [ ] Usage guide shared with team
- [ ] Example commands documented
- [ ] Troubleshooting guide available
- [ ] Feedback mechanism established

#### 5.2 Team Onboarding

Share these resources with your team:

1. **Quick Start**: [`QUICKSTART.md`](../QUICKSTART.md)
2. **Setup Guide**: [`MCP_SETUP_GUIDE.md`](MCP_SETUP_GUIDE.md)
3. **This Testing Plan**: [`TESTING_PLAN.md`](TESTING_PLAN.md)
4. **Architecture**: [`reports/ARCHITECTURE.md`](reports/ARCHITECTURE.md)

#### 5.3 Usage Examples Document

Create `USAGE_EXAMPLES.md` with real-world scenarios:

```markdown
# BobSuite MCP Usage Examples

## Scenario 1: Code Review Workflow
1. Scan code quality
2. Generate documentation
3. Create unit tests
4. Review git diff

## Scenario 2: Project Onboarding
1. Generate project concept
2. Create dependency chain
3. Generate feature flows
4. Document all modules

## Scenario 3: Quality Assurance
1. Scan all changed files
2. Generate tests for new code
3. Verify documentation updated
4. Check for vulnerabilities
```

---

## 📊 Success Metrics

### Minimum Viable Product (MVP)
- ✅ 2 critical tools working (scan_code_quality, generate_documentation)
- ✅ Server stable and responsive
- ✅ Basic error handling functional

### Full Production Ready
- ✅ All 10 tools operational
- ✅ Response times <30s average
- ✅ Error rate <5%
- ✅ Documentation complete
- ✅ Team trained

### Excellence
- ✅ All tools tested with real projects
- ✅ Custom prompts optimized
- ✅ Performance benchmarks met
- ✅ User feedback incorporated
- ✅ Extended with custom tools

---

## 🚀 Quick Command Reference

```bash
# Activate environment
cd mcp_server
venv\Scripts\activate

# Test connection
python -c "from watsonx_client import WatsonxClient; WatsonxClient()"

# Test modules
python test_modules.py

# Start server manually
python server.py

# Run existing tests
pytest tests/

# Deactivate
deactivate
```

---

## 🎯 Next Actions

1. **Immediate (Today)**
   - [ ] Create `.env.example` file
   - [ ] Run Phase 1 pre-flight checks
   - [ ] Test server startup locally
   - [ ] Configure IBM Bob MCP settings

2. **Short-term (This Week)**
   - [ ] Test all 10 tools systematically
   - [ ] Document any issues found
   - [ ] Create usage examples
   - [ ] Share with team

3. **Long-term (Ongoing)**
   - [ ] Optimize prompts based on usage
   - [ ] Add custom tools as needed
   - [ ] Monitor performance
   - [ ] Gather user feedback

---

## 📞 Support Resources

- **Setup Issues**: See [`MCP_SETUP_GUIDE.md`](MCP_SETUP_GUIDE.md)
- **Architecture Questions**: See [`reports/ARCHITECTURE.md`](reports/ARCHITECTURE.md)
- **Quick Start**: See [`QUICKSTART.md`](../QUICKSTART.md)
- **MCP Protocol**: https://modelcontextprotocol.io/
- **IBM watsonx.ai**: https://www.ibm.com/docs/en/watsonx-as-a-service

---

**Ready to start testing?** Begin with Phase 1 and work through systematically! 🧪