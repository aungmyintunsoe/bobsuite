# 🚀 Step-by-Step MCP Server Setup & Testing

**Complete hands-on guide to get your MCP server running with IBM Bob**

---

## 📋 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ IBM Cloud account with watsonx.ai access
- ✅ IBM Bob IDE installed
- ✅ Your `.env` file with credentials (already done ✓)

---

## 🔧 STEP 1: Test Your Setup Locally

### 1.1 Open Terminal in Project Directory

```bash
cd d:/bobsuite/mcp_server
```

### 1.2 Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 1.3 Install/Verify Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Requirement already satisfied: mcp>=0.9.0
Requirement already satisfied: python-dotenv>=1.0.0
...
```

### 1.4 Run Setup Test Script

```bash
python test_mcp_setup.py
```

**Expected output:**
```
============================================================
MCP SERVER SETUP TEST
============================================================

============================================================
STEP 1: Testing Module Imports
============================================================
✓ WatsonxClient imported
✓ QASentry imported
✓ AutoDocs imported
✓ IdeationEngine imported
✓ VisualizerEngine imported
✓ MCP Server imported

✓ All imports successful!

============================================================
STEP 2: Testing Watsonx Connection
============================================================
✓ WatsonxClient initialized
  API Key: pak-xxxxx...
  Project ID: your-project-id
  URL: https://us-south.ml.cloud.ibm.com
✓ Successfully obtained access token
  Token: eyJraWQiOiIyMDI0...

✓ Watsonx connection successful!

============================================================
STEP 3: Testing Module Initialization
============================================================
✓ QASentry initialized
✓ AutoDocs initialized
✓ IdeationEngine initialized
✓ VisualizerEngine initialized

✓ All modules initialized successfully!

============================================================
STEP 4: Testing MCP Server
============================================================
✓ BobSuiteMCPServer initialized
  Server name: bobsuite-mcp
  Tools registered: 10 expected

✓ MCP Server ready!

============================================================
✅ ALL TESTS PASSED!
============================================================

Your MCP server is ready to use with IBM Bob!
```

**If you see errors:**
- ❌ Import errors → Run `pip install -r requirements.txt`
- ❌ Credential errors → Check your `.env` file
- ❌ Connection errors → Verify your IBM API key is valid

---

## 🔌 STEP 2: Configure IBM Bob MCP Settings

### 2.1 Find Your MCP Settings File

**Option A: Via IBM Bob UI**
1. Open IBM Bob
2. Press `Ctrl+,` (or `Cmd+,` on Mac) to open Settings
3. Search for "MCP" in the search bar
4. Click "Edit in settings.json"

**Option B: Manual File Location**

**Windows:**
```
%APPDATA%\Code\User\globalStorage\ibm.bob\settings.json
```

**Mac:**
```
~/Library/Application Support/Code/User/globalStorage/ibm.bob/settings.json
```

**Linux:**
```
~/.config/Code/User/globalStorage/ibm.bob/settings.json
```

### 2.2 Add BobSuite MCP Server Configuration

Open the settings file and add this configuration:

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

**To find your project path:**
```bash
# In your terminal (from mcp_server directory)
cd ..
pwd  # Mac/Linux
cd   # Windows
```

### 2.3 Alternative Configurations

**If Python is not in your PATH:**
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

**If using virtual environment directly:**
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

### 2.4 Save and Close the Settings File

---

## 🔄 STEP 3: Restart IBM Bob

1. **Close all IBM Bob windows completely**
2. **Restart IBM Bob**
3. **Wait for it to fully load** (about 10-15 seconds)

---

## 🔍 STEP 4: Verify MCP Server Connection

### 4.1 Check Output Panel

1. In IBM Bob, go to **View → Output** (or press `Ctrl+Shift+U`)
2. In the dropdown at the top right, select **"MCP"**
3. Look for these messages:

**Expected logs:**
```
[MCP] Starting server: bobsuite
[MCP] Server bobsuite connected successfully
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

### 4.2 Troubleshooting Connection Issues

**If you see "Server failed to start":**
1. Check the Python path in your MCP settings
2. Verify `server.py` path is correct
3. Try running `python d:/bobsuite/mcp_server/server.py` manually
4. Check for error messages in the Output panel

**If you see "No tools discovered":**
1. Check for syntax errors in `server.py`
2. Verify all imports work (run `test_mcp_setup.py` again)
3. Check the Output panel for specific error messages

---

## 🧪 STEP 5: Test Individual Tools

Now let's test each tool systematically. Open IBM Bob chat and try these commands:

### Test 1: scan_code_quality (CRITICAL - Test First!)

**Command:**
```
Bob, use scan_code_quality to analyze mcp_server/server.py with scan_type "quality"
```

**What to expect:**
- Response time: 10-30 seconds
- Output: Markdown report with code quality analysis
- Should include: suggestions, code snippets, quality metrics

**Success criteria:**
- ✅ No errors
- ✅ Receives markdown report
- ✅ Report contains actual analysis (not just "analyzing...")

---

### Test 2: generate_documentation (CRITICAL)

**Command:**
```
Bob, generate documentation for mcp_server/watsonx_client.py with doc_type "api"
```

**What to expect:**
- Response time: 15-40 seconds
- Output: API documentation in markdown
- Should include: class descriptions, method signatures, parameters

**Success criteria:**
- ✅ No errors
- ✅ Receives formatted documentation
- ✅ Documentation is accurate and complete

---

### Test 3: generate_project_concept (IMPORTANT)

**Command:**
```
Bob, generate a project concept map for the mcp_server directory
```

**What to expect:**
- Response time: 20-45 seconds
- Output: Mermaid diagram showing architecture
- Should include: component relationships, high-level overview

**Success criteria:**
- ✅ No errors
- ✅ Receives Mermaid diagram
- ✅ Diagram renders correctly in markdown preview

---

### Test 4: generate_dependency_chain (IMPORTANT)

**Command:**
```
Bob, generate a dependency chain for mcp_server with max_depth 2
```

**What to expect:**
- Response time: 20-45 seconds
- Output: Dependency diagram showing imports
- Should include: module relationships, import chains

**Success criteria:**
- ✅ No errors
- ✅ Receives dependency diagram
- ✅ Shows actual project dependencies

---

### Test 5: generate_unit_tests (IMPORTANT)

**Command:**
```
Bob, generate unit tests for mcp_server/watsonx_client.py
```

**What to expect:**
- Response time: 30-60 seconds
- Output: Complete pytest test file
- Should include: test cases, mocks, assertions

**Success criteria:**
- ✅ No errors
- ✅ Receives complete test file
- ✅ Tests follow best practices

---

### Test 6: scan_git_diff (OPTIONAL)

**Command:**
```
Bob, use scan_git_diff to analyze changes in d:/bobsuite with staged set to true
```

**What to expect:**
- Response time: 15-30 seconds
- Output: Analysis of git changes
- Should include: quality assessment, suggestions

**Success criteria:**
- ✅ No errors (or "no changes" if nothing staged)
- ✅ Receives analysis report
- ✅ Identifies actual changes

---

### Test 7: get_project_framework (SIMPLE)

**Command:**
```
Bob, use get_project_framework with include_examples set to true
```

**What to expect:**
- Response time: <5 seconds (no AI call)
- Output: 7-pillar ideation framework
- Should include: framework structure, examples

**Success criteria:**
- ✅ No errors
- ✅ Receives framework immediately
- ✅ Shows all 7 pillars

---

### Test 8: generate_feature_flow (OPTIONAL)

**Command:**
```
Bob, generate a feature flow map for the mcp_server directory
```

**What to expect:**
- Response time: 25-50 seconds
- Output: Feature flow diagram
- Should include: user journeys, data flows

**Success criteria:**
- ✅ No errors
- ✅ Receives flow diagram
- ✅ Shows logical feature flows

---

### Test 9: synthesize_project_plan (ADVANCED)

**Command:**
```
Bob, use synthesize_project_plan with conversation_data containing a simple project idea
```

**What to expect:**
- Response time: 40-90 seconds
- Output: Complete PRD document
- Should include: requirements, architecture, timeline

**Success criteria:**
- ✅ No errors
- ✅ Receives PRD document
- ✅ PRD is comprehensive

---

### Test 10: generate_network_performance_tests (OPTIONAL)

**Command:**
```
Bob, generate network performance tests for mcp_server/watsonx_client.py
```

**What to expect:**
- Response time: 30-60 seconds
- Output: Network/API test file
- Should include: performance tests, timeout handling

**Success criteria:**
- ✅ No errors
- ✅ Receives test file
- ✅ Tests are relevant to network operations

---

## 📊 STEP 6: Record Your Test Results

Create a file `test_results.md` and record your results:

```markdown
# MCP Server Test Results

**Date:** [Today's Date]
**Tester:** [Your Name]

## Environment
- Python Version: [Your version]
- MCP Version: [Check with pip show mcp]
- IBM Bob Version: [Your version]

## Test Results

| # | Tool | Status | Response Time | Notes |
|---|------|--------|---------------|-------|
| 1 | scan_code_quality | ✅/❌ | Xs | |
| 2 | generate_documentation | ✅/❌ | Xs | |
| 3 | generate_project_concept | ✅/❌ | Xs | |
| 4 | generate_dependency_chain | ✅/❌ | Xs | |
| 5 | generate_unit_tests | ✅/❌ | Xs | |
| 6 | scan_git_diff | ✅/❌ | Xs | |
| 7 | get_project_framework | ✅/❌ | Xs | |
| 8 | generate_feature_flow | ✅/❌ | Xs | |
| 9 | synthesize_project_plan | ✅/❌ | Xs | |
| 10 | generate_network_performance_tests | ✅/❌ | Xs | |

## Summary
- **Tools Working:** X/10
- **Critical Tools (1-2):** ✅/❌
- **Important Tools (3-5):** ✅/❌
- **Optional Tools (6-10):** ✅/❌

## Issues Found
[List any issues]

## Next Steps
[What to do next]
```

---

## 🎯 Success Criteria

### Minimum Viable (MVP)
- ✅ Server connects to IBM Bob
- ✅ At least 2 critical tools work (scan_code_quality, generate_documentation)
- ✅ No connection errors

### Production Ready
- ✅ All 10 tools operational
- ✅ Average response time <45 seconds
- ✅ Error rate <10%
- ✅ Documentation complete

### Excellence
- ✅ All tools tested with real projects
- ✅ Response times optimized
- ✅ Custom prompts tuned
- ✅ Team trained on usage

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found"
**Solution:**
```bash
cd mcp_server
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Invalid credentials"
**Solution:**
1. Check `.env` file exists in `mcp_server/`
2. Verify API key format (should start with "pak-")
3. Verify project ID is correct
4. Try regenerating API key in IBM Cloud

### Issue: "Server timeout"
**Solution:**
1. Check internet connection
2. Verify watsonx.ai service is up
3. Try with smaller files first
4. Check firewall settings

### Issue: "Tools not discovered"
**Solution:**
1. Check Output panel for errors
2. Verify `server.py` has no syntax errors
3. Run `python test_mcp_setup.py` again
4. Check MCP settings path is correct

---

## 📚 Next Steps After Testing

### 1. Document Your Findings
- Save test results to `bob_sessions/`
- Note any issues or improvements
- Share with team

### 2. Optimize Performance
- Adjust prompts in `lib/*/prompts.py`
- Tune model parameters if needed
- Cache frequently used results

### 3. Extend Functionality
- Add custom tools to `server.py`
- Create project-specific analyzers
- Integrate additional services

### 4. Train Your Team
- Share usage examples
- Create workflow guides
- Document best practices

---

## 🎓 Usage Examples for Real Work

### Example 1: Code Review Workflow
```
Bob, I need a comprehensive code review:
1. Use scan_code_quality on src/main.py
2. Generate documentation for src/main.py
3. Generate unit tests for src/main.py
4. Scan git diff to check my changes
```

### Example 2: Project Onboarding
```
Bob, help me understand this project:
1. Generate a project concept map for the entire codebase
2. Create a dependency chain diagram
3. Generate feature flow for the authentication module
```

### Example 3: Documentation Sprint
```
Bob, document the entire project:
1. Generate API docs for all modules in src/
2. Create a comprehensive README
3. Generate usage examples for each feature
```

---

## ✅ Final Checklist

Before considering setup complete:

- [ ] `test_mcp_setup.py` passes all tests
- [ ] IBM Bob MCP settings configured
- [ ] Server appears in IBM Bob Output panel
- [ ] 10 tools discovered successfully
- [ ] At least 2 critical tools tested and working
- [ ] Test results documented
- [ ] Team members can access (if applicable)
- [ ] Usage examples created
- [ ] Troubleshooting guide reviewed

---

## 🚀 You're Ready!

Once you've completed all steps and tests, your MCP server is production-ready!

**Start using it for:**
- 🔍 Code quality analysis
- 📝 Automatic documentation
- 🧪 Test generation
- 📊 Project visualization
- 🎯 Feature planning

**Happy coding with IBM Bob! 🎉**