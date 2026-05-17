# 👥 Team Setup Guide - BobSuite MCP Server

**Quick setup guide for hackathon team members**

---

## 🎯 What You're Setting Up

An MCP server that gives IBM Bob superpowers:
- 🔍 AI-powered code analysis
- 📝 Automatic documentation generation
- 🧪 Smart test generation
- 📊 Project visualization

---

## ⚡ Quick Setup (15 minutes)

### Prerequisites

- ✅ Python 3.8 or higher
- ✅ IBM Bob IDE installed
- ✅ IBM Cloud account with watsonx.ai access
- ✅ Git installed

---

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd bobsuite
```

---

### Step 2: Set Up Python Environment

```bash
cd mcp_server

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed mcp-0.9.0 python-dotenv-1.0.0 httpx-0.24.0 ...
```

---

### Step 3: Configure Your Credentials

```bash
# Copy the template
cp .env.example .env

# Edit .env with your credentials
notepad .env  # Windows
nano .env     # Mac/Linux
```

**Add your IBM credentials:**

```env
IBM_API_KEY=your_api_key_here
PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Where to get these:**

1. **IBM_API_KEY**
   - Go to: https://cloud.ibm.com/
   - Click: Manage → Access (IAM) → API keys
   - Create or copy your API key

2. **PROJECT_ID**
   - Go to: https://watsonx.ai/
   - Click: Projects → Your Project → Settings
   - Copy the Project ID

---

### Step 4: Test Your Setup

```bash
python test_mcp_setup.py
```

**Expected output:**
```
============================================================
[SUCCESS] ALL TESTS PASSED!
============================================================

Your MCP server is ready to use with IBM Bob!
```

**If you see errors:**
- ❌ Import errors → Run `pip install -r requirements.txt` again
- ❌ Credential errors → Check your `.env` file
- ❌ Connection errors → Verify your IBM API key is valid

---

### Step 5: Configure IBM Bob

**Find your project path:**

```bash
# Windows
cd

# Mac/Linux
pwd
```

Copy the path (e.g., `c:/Users/yourname/bobsuite`)

**Configure MCP settings:**

**Option A: Via IBM Bob UI**
1. Open IBM Bob
2. Press `Ctrl+,` (Settings)
3. Search for "MCP"
4. Click "Edit in settings.json"

**Option B: Manual**
- **Windows:** `%APPDATA%\Code\User\globalStorage\ibm.bob\settings.json`
- **Mac:** `~/Library/Application Support/Code/User/globalStorage/ibm.bob/settings.json`
- **Linux:** `~/.config/Code/User/globalStorage/ibm.bob/settings.json`

**Add this configuration (replace `<YOUR_PATH>` with your actual path):**

```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["<YOUR_PATH>/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "<YOUR_PATH>/mcp_server"
      }
    }
  }
}
```

**Examples:**

**Windows:**
```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["c:/Users/john/bobsuite/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "c:/Users/john/bobsuite/mcp_server"
      }
    }
  }
}
```

**Mac/Linux:**
```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["/home/jane/bobsuite/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "/home/jane/bobsuite/mcp_server"
      }
    }
  }
}
```

---

### Step 6: Restart IBM Bob

1. Close all IBM Bob windows
2. Restart IBM Bob
3. Wait 10-15 seconds

---

### Step 7: Verify Connection

**Check Output Panel:**
1. View → Output (or `Ctrl+Shift+U`)
2. Select "MCP" from dropdown
3. Look for:

```
[MCP] Starting server: bobsuite
[MCP] Server bobsuite connected
[MCP] Discovered 10 tools from bobsuite
```

**If you see errors:**
- Check the path in your MCP settings
- Verify Python is in your PATH
- See troubleshooting section below

---

### Step 8: Test Your First Tool

In IBM Bob chat, type:

```
Bob, use scan_code_quality to analyze mcp_server/server.py with scan_type "quality"
```

**Expected:**
- Response in 10-30 seconds
- Markdown report with code analysis
- Suggestions and improvements

**If it works:** 🎉 You're all set!

---

## 🧪 Test All Tools

Try these commands in IBM Bob:

### 1. Code Quality Scanner
```
Bob, scan dataset_balancia/src/app/actions/profileActions.ts for bugs
```

### 2. Documentation Generator
```
Bob, generate documentation for dataset_balancia/src/lib/utils.ts with doc_type "api"
```

### 3. Project Concept Map
```
Bob, generate a project concept map for dataset_balancia
```

### 4. Dependency Chain
```
Bob, generate a dependency chain for dataset_balancia with max_depth 2
```

### 5. Unit Test Generator
```
Bob, generate unit tests for dataset_balancia/src/app/actions/profileActions.ts
```

---

## 🐛 Troubleshooting

### Issue: "Module not found"

**Solution:**
```bash
cd mcp_server
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Invalid credentials"

**Solution:**
1. Check `.env` file exists in `mcp_server/`
2. Verify API key format (should start with "pak-" or similar)
3. Verify project ID is correct
4. Try regenerating API key in IBM Cloud

### Issue: "Server failed to start"

**Solution:**
1. Check Python is in PATH: `python --version`
2. Verify path in MCP settings is correct
3. Try using full Python path:
   ```json
   "command": "C:/Python39/python.exe"
   ```
4. Or use venv path:
   ```json
   "command": "c:/Users/yourname/bobsuite/mcp_server/venv/Scripts/python.exe"
   ```

### Issue: "No tools discovered"

**Solution:**
1. Check Output panel for specific errors
2. Run test again: `python test_mcp_setup.py`
3. Verify `server.py` has no syntax errors
4. Restart IBM Bob

### Issue: "Tool execution failed"

**Solution:**
1. Check internet connection
2. Verify watsonx.ai service is up
3. Try with smaller files first
4. Check Output panel for error details

---

## 📝 Important Notes

### ⚠️ DO NOT Commit These Files

```
mcp_server/.env          # Has your credentials!
.bob/mcp.json           # Has your local paths!
mcp_server/venv/        # Virtual environment
```

### ✅ DO Commit These Files

```
mcp_server/server.py
mcp_server/requirements.txt
mcp_server/.env.example
mcp_server/lib/
All documentation
dataset_balancia/
```

### 🔒 Security

- **Never share your `.env` file**
- **Never commit credentials to git**
- **Each person uses their own IBM API key**

---

## 💡 How to Use the Tools

### Basic Pattern

```
Bob, use <tool_name> to <action> <file_path> with <parameters>
```

### File Paths

**✅ Correct (relative to workspace root):**
```
dataset_balancia/src/app/actions/profileActions.ts
mcp_server/server.py
README.md
```

**❌ Incorrect:**
```
../dataset_balancia/...  # Don't use ../
d:/bobsuite/...          # Don't use absolute paths
/dataset_balancia/...    # Don't use leading /
```

### Example Workflows

**Code Review Before Commit:**
```
Bob, review my changes:
1. Use scan_git_diff to check what changed
2. Scan code quality on modified files
3. Generate tests for new code
```

**Project Onboarding:**
```
Bob, help me understand this project:
1. Generate project concept map
2. Show dependency chain
3. Create feature flow diagram
```

**Documentation Sprint:**
```
Bob, document everything:
1. Generate API docs for all modules
2. Create comprehensive README
3. Add usage examples
```

---

## 🎯 Success Checklist

- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured with your credentials
- [ ] `test_mcp_setup.py` passes all tests
- [ ] IBM Bob MCP settings configured with your path
- [ ] IBM Bob restarted
- [ ] Server connected (check Output panel)
- [ ] First tool tested successfully
- [ ] All 10 tools working

---

## 📚 Additional Resources

| Document | Purpose |
|----------|---------|
| [HOW_MCP_WORKS.md](HOW_MCP_WORKS.md) | Understanding MCP architecture |
| [STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md) | Detailed setup guide |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Command reference |
| [NEXT_STEPS.md](NEXT_STEPS.md) | What to do after setup |

---

## 🆘 Need Help?

1. **Check Output Panel** in IBM Bob for error messages
2. **Run test script**: `python test_mcp_setup.py`
3. **Review troubleshooting** section above
4. **Ask team lead** or check documentation

---

## 🚀 You're Ready!

Once setup is complete, you can:
- 🔍 Analyze code quality with AI
- 📝 Generate documentation automatically
- 🧪 Create smart tests
- 📊 Visualize project architecture
- 🎯 Plan features systematically

**All powered by IBM watsonx.ai! 🎉**

---

**Questions? Check [HOW_MCP_WORKS.md](HOW_MCP_WORKS.md) for detailed explanations!**