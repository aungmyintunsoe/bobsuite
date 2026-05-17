# 🔌 How MCP Servers Work - Complete Guide

**Understanding the Model Context Protocol and how to use your BobSuite MCP server**

---

## 🤔 What You Were Trying to Do (And Why It Didn't Work)

### ❌ What You Did (Incorrect)
```python
# Created scan_profile_actions.py to manually call the server
# This bypasses the MCP protocol entirely
```

### ✅ What You Should Do (Correct)
```
# In IBM Bob chat, just type:
Bob, use scan_code_quality to analyze dataset_balancia/src/app/actions/profileActions.ts with scan_type "all"
```

**Why?** MCP servers are designed to be called BY IBM Bob, not run manually!

---

## 📚 Understanding MCP Architecture

### How It Works

```
┌─────────────┐         MCP Protocol        ┌──────────────┐
│             │◄──────────────────────────►│              │
│  IBM Bob    │   (stdio communication)     │  MCP Server  │
│             │                             │  (server.py) │
└─────────────┘                             └──────────────┘
      │                                            │
      │ 1. User types command                     │
      │ 2. Bob discovers tools                    │
      │ 3. Bob calls tool                         │
      │ 4. Server processes                       │
      │ 5. Server returns result                  │
      │ 6. Bob shows result                       │
      └───────────────────────────────────────────┘
```

### Key Points

1. **MCP Server = Background Service**
   - Runs automatically when IBM Bob starts
   - Listens for tool calls via stdio
   - You never run it manually (except for testing)

2. **IBM Bob = Client**
   - Discovers available tools from the server
   - Sends requests when you use tools
   - Displays results to you

3. **You = User**
   - Just chat with Bob naturally
   - Bob handles all MCP communication
   - You see the results

---

## 🎯 The Correct Way to Use MCP Tools

### Step 1: Ensure Server is Running

**Check IBM Bob Output Panel:**
1. Open IBM Bob
2. View → Output (Ctrl+Shift+U)
3. Select "MCP" from dropdown
4. Look for:
```
[MCP] Starting server: bobsuite
[MCP] Server bobsuite connected
[MCP] Discovered 10 tools from bobsuite
```

### Step 2: Use Tools in Chat

**Just talk to Bob naturally:**

```
Bob, scan dataset_balancia/src/app/actions/profileActions.ts for code quality issues
```

**Or be more specific:**

```
Bob, use scan_code_quality to analyze dataset_balancia/src/app/actions/profileActions.ts with scan_type "all"
```

**Bob will:**
1. Recognize you want to use `scan_code_quality`
2. Call the MCP server with the file path
3. Wait for the analysis
4. Show you the results

### Step 3: Review Results

Bob will display the analysis directly in the chat!

---

## 📁 File Paths: How They Work

### Important: Paths are Relative to Workspace Root

Your workspace root is: `d:/bobsuite`

**Correct paths:**
```
dataset_balancia/src/app/actions/profileActions.ts  ✓
mcp_server/server.py  ✓
README.md  ✓
```

**Incorrect paths:**
```
../dataset_balancia/src/app/actions/profileActions.ts  ✗ (don't use ../)
d:/bobsuite/dataset_balancia/...  ✗ (don't use absolute paths)
/dataset_balancia/...  ✗ (don't use leading /)
```

**Why?** The MCP server runs with `d:/bobsuite` as the working directory.

---

## 👥 Team Setup: How Each Person Configures

### The Problem
Each team member has a different path to the project!

**Your path:** `d:/bobsuite`  
**Teammate 1:** `c:/Users/john/projects/bobsuite`  
**Teammate 2:** `/home/jane/bobsuite`  

### The Solution

Each person needs to:

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd bobsuite
```

2. **Set up their own `.env` file**
```bash
cd mcp_server
cp .env.example .env
# Edit .env with THEIR OWN IBM credentials
```

3. **Configure MCP settings with THEIR path**

**Location:** `.bob/mcp.json` (or IBM Bob settings)

```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["<THEIR_PATH>/mcp_server/server.py"],
      "env": {"PYTHONPATH": "<THEIR_PATH>/mcp_server"}
    }
  }
}
```

**Examples:**

**Windows user:**
```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["c:/Users/john/projects/bobsuite/mcp_server/server.py"],
      "env": {"PYTHONPATH": "c:/Users/john/projects/bobsuite/mcp_server"}
    }
  }
}
```

**Mac/Linux user:**
```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["/home/jane/bobsuite/mcp_server/server.py"],
      "env": {"PYTHONPATH": "/home/jane/bobsuite/mcp_server"}
    }
  }
}
```

4. **Install dependencies**
```bash
cd mcp_server
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

5. **Test setup**
```bash
python test_mcp_setup.py
```

---

## 🗂️ Project Structure: What Goes Where

### Your Repository Structure

```
bobsuite/                          ← Git repository root
├── .bob/
│   └── mcp.json                   ← MCP configuration (gitignored)
├── mcp_server/                    ← The MCP server (shared)
│   ├── .env                       ← Credentials (gitignored)
│   ├── .env.example               ← Template (committed)
│   ├── server.py                  ← MCP server (committed)
│   ├── requirements.txt           ← Dependencies (committed)
│   └── lib/                       ← Tool implementations (committed)
├── dataset_balancia/              ← Your project to analyze (committed)
└── README.md                      ← Documentation (committed)
```

### What to Commit to Git

**✅ Commit these:**
- `mcp_server/server.py`
- `mcp_server/requirements.txt`
- `mcp_server/.env.example`
- `mcp_server/lib/` (all tool code)
- All documentation
- `dataset_balancia/` (your project)

**❌ Don't commit these:**
- `mcp_server/.env` (has credentials!)
- `.bob/mcp.json` (has local paths!)
- `mcp_server/venv/` (virtual environment)
- `mcp_server/__pycache__/`

### Your `.gitignore` Should Have

```gitignore
# Credentials
mcp_server/.env
**/.env
*.key
*.pem

# MCP configuration (local paths)
.bob/mcp.json

# Python
__pycache__/
*.pyc
venv/
.pytest_cache/

# IDE
.vscode/
.idea/
```

---

## 📖 Team Onboarding Guide

### For New Team Members

**Create this file: `TEAM_SETUP.md`**

```markdown
# Team Setup Guide

## Prerequisites
- Python 3.8+
- IBM Bob IDE
- IBM Cloud account with watsonx.ai access

## Setup Steps

### 1. Clone Repository
\`\`\`bash
git clone <repo-url>
cd bobsuite
\`\`\`

### 2. Set Up MCP Server
\`\`\`bash
cd mcp_server
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
\`\`\`

### 3. Configure Credentials
\`\`\`bash
cp .env.example .env
# Edit .env with YOUR IBM credentials
\`\`\`

Get credentials from:
- IBM_API_KEY: IBM Cloud → Manage → Access (IAM) → API keys
- PROJECT_ID: watsonx.ai → Projects → Your Project → Settings

### 4. Test Setup
\`\`\`bash
python test_mcp_setup.py
\`\`\`

Should see: `[SUCCESS] ALL TESTS PASSED!`

### 5. Configure IBM Bob

**Option A: Via UI**
1. Open IBM Bob
2. Settings (Ctrl+,) → Search "MCP"
3. Edit in settings.json

**Option B: Manual**
Edit: `%APPDATA%\Code\User\globalStorage\ibm.bob\settings.json`

Add (replace with YOUR path):
\`\`\`json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["<YOUR_PATH>/mcp_server/server.py"],
      "env": {"PYTHONPATH": "<YOUR_PATH>/mcp_server"}
    }
  }
}
\`\`\`

### 6. Restart IBM Bob

### 7. Test in Chat
\`\`\`
Bob, use scan_code_quality to analyze mcp_server/server.py with scan_type "quality"
\`\`\`

## Troubleshooting
See [STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)
```

---

## 🧪 Testing: The Right Way

### ❌ Wrong Way (What You Did)
```python
# Creating scripts to manually call server functions
# This bypasses MCP and doesn't test the real integration
```

### ✅ Right Way

**1. Test Server Locally**
```bash
cd mcp_server
python test_mcp_setup.py
```

**2. Test via IBM Bob**
```
Bob, use scan_code_quality to analyze dataset_balancia/src/app/actions/profileActions.ts with scan_type "all"
```

**3. Verify Results**
- Check you get a markdown report
- Verify analysis is accurate
- Confirm no errors

---

## 🔧 Your Current Setup

### What You Have

**✅ Correct:**
- `.bob/mcp.json` exists with correct configuration
- Path is correct: `d:/bobsuite/mcp_server/server.py`
- Server tested and working

**❌ To Fix:**
- Delete `mcp_server/scan_profile_actions.py` (already done ✓)
- Don't create manual scripts to call the server
- Use IBM Bob chat interface instead

### Next Steps

1. **Restart IBM Bob** (if not already done)
2. **Check Output panel** for MCP connection
3. **Test in chat:**
```
Bob, use scan_code_quality to analyze dataset_balancia/src/app/actions/profileActions.ts with scan_type "all"
```

---

## 💡 Common Mistakes & Solutions

### Mistake 1: Running Server Manually
```bash
python mcp_server/server.py  # ❌ Don't do this
```
**Solution:** Let IBM Bob start it automatically

### Mistake 2: Creating Scripts to Call Tools
```python
# scan_profile_actions.py  # ❌ Don't do this
```
**Solution:** Use IBM Bob chat interface

### Mistake 3: Using Absolute Paths
```
Bob, scan d:/bobsuite/dataset_balancia/...  # ❌
```
**Solution:** Use relative paths from workspace root
```
Bob, scan dataset_balancia/...  # ✓
```

### Mistake 4: Sharing .env Files
```bash
git add mcp_server/.env  # ❌ NEVER!
```
**Solution:** Each person creates their own from `.env.example`

### Mistake 5: Committing Local Paths
```bash
git add .bob/mcp.json  # ❌ Don't commit
```
**Solution:** Add to `.gitignore`, each person configures their own

---

## 📝 Quick Reference

### To Use a Tool
```
Bob, use <tool_name> to <action> <file_path> with <parameters>
```

### Available Tools
1. `scan_code_quality` - Analyze code
2. `generate_documentation` - Create docs
3. `generate_project_concept` - Architecture diagram
4. `generate_dependency_chain` - Module relationships
5. `generate_unit_tests` - Test generation
6. `scan_git_diff` - Git change analysis
7. `get_project_framework` - Ideation framework
8. `generate_feature_flow` - User journeys
9. `synthesize_project_plan` - PRD generation
10. `generate_network_performance_tests` - API tests

### Example Commands
```
Bob, scan dataset_balancia/src/app/actions/profileActions.ts for bugs

Bob, generate documentation for dataset_balancia/src/lib/utils.ts

Bob, create a project concept map for dataset_balancia

Bob, generate unit tests for dataset_balancia/src/app/actions/profileActions.ts
```

---

## 🎯 Summary

**Key Takeaways:**

1. **MCP servers run in the background** - IBM Bob starts them automatically
2. **Use tools via chat** - Don't create manual scripts
3. **Paths are relative** - From workspace root (`d:/bobsuite`)
4. **Each person configures their own** - Paths and credentials are local
5. **Don't commit credentials or local paths** - Use `.gitignore`

**You're ready to use the MCP server! Just chat with Bob! 🚀**