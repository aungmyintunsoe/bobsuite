# 🎯 How to Use MCP Tools - The Right Way

**Stop creating manual scripts! Just chat with IBM Bob!**

---

## ❌ WRONG: What You've Been Trying

```python
# Creating run_scan.py, scan_profile_actions.py, etc.
# Running: python run_scan.py
# This is WRONG and unnecessary!
```

**Why it's wrong:**
- Bypasses the MCP protocol
- Requires manual script creation for each task
- Defeats the purpose of having an MCP server
- More work for you!

---

## ✅ RIGHT: How to Actually Use It

### Step 1: Ensure IBM Bob is Running

1. Open IBM Bob
2. Check Output panel (View → Output or Ctrl+Shift+U)
3. Select "MCP" from dropdown
4. Verify you see:
```
[MCP] Server bobsuite connected
[MCP] Discovered 10 tools from bobsuite
```

### Step 2: Just Chat with Bob!

**That's it! Just type in the chat!**

---

## 📝 Example Commands

### Scan Code Quality

**Natural language:**
```
Bob, scan mcp_server/watsonx_client.py for bugs and quality issues
```

**Explicit tool call:**
```
Bob, use scan_code_quality to analyze mcp_server/watsonx_client.py with scan_type "all"
```

**What happens:**
1. You type the command
2. Bob recognizes you want to use `scan_code_quality`
3. Bob calls the MCP server automatically
4. Server analyzes the file
5. Bob shows you the results
6. Done!

---

### Generate Documentation

**Natural language:**
```
Bob, document the watsonx_client.py file
```

**Explicit tool call:**
```
Bob, generate documentation for mcp_server/watsonx_client.py with doc_type "api"
```

---

### Generate Unit Tests

**Natural language:**
```
Bob, create unit tests for dataset_balancia/src/app/actions/profileActions.ts
```

**Explicit tool call:**
```
Bob, generate unit tests for dataset_balancia/src/app/actions/profileActions.ts
```

---

### Project Visualization

**Natural language:**
```
Bob, show me the architecture of dataset_balancia
```

**Explicit tool call:**
```
Bob, generate a project concept map for dataset_balancia
```

---

## 🎯 All 10 Available Tools

| # | Tool | How to Use |
|---|------|------------|
| 1 | **scan_code_quality** | `Bob, scan <file> for bugs` |
| 2 | **generate_documentation** | `Bob, document <file>` |
| 3 | **generate_project_concept** | `Bob, show architecture of <dir>` |
| 4 | **generate_dependency_chain** | `Bob, show dependencies in <dir>` |
| 5 | **generate_unit_tests** | `Bob, create tests for <file>` |
| 6 | **scan_git_diff** | `Bob, check my git changes` |
| 7 | **get_project_framework** | `Bob, show ideation framework` |
| 8 | **generate_feature_flow** | `Bob, show feature flow for <dir>` |
| 9 | **synthesize_project_plan** | `Bob, create PRD from <conversation>` |
| 10 | **generate_network_performance_tests** | `Bob, create API tests for <file>` |

---

## 🔍 File Paths

**Important:** Paths are relative to workspace root (`d:/bobsuite`)

### ✅ Correct Paths

```
mcp_server/watsonx_client.py
dataset_balancia/src/app/actions/profileActions.ts
README.md
```

### ❌ Incorrect Paths

```
../mcp_server/watsonx_client.py  # Don't use ../
d:/bobsuite/mcp_server/...       # Don't use absolute paths
/mcp_server/...                  # Don't use leading /
```

---

## 🐛 Troubleshooting

### "Tool not found" or "No tools available"

**Check:**
1. Is IBM Bob running?
2. Is MCP server connected? (Check Output panel)
3. Did you restart IBM Bob after configuring MCP settings?

**Fix:**
1. Restart IBM Bob
2. Check `.bob/mcp.json` has correct configuration
3. Verify `python mcp_server/test_mcp_setup.py` passes

---

### "File not found" error

**Check:**
- Are you using relative paths from workspace root?
- Does the file actually exist?

**Fix:**
```
# Wrong:
Bob, scan ../dataset_balancia/src/app/actions/profileActions.ts

# Right:
Bob, scan dataset_balancia/src/app/actions/profileActions.ts
```

---

### Tool execution fails

**Check:**
1. Is your `.env` file configured?
2. Are your IBM credentials valid?
3. Is internet connection working?

**Fix:**
1. Run `python mcp_server/test_mcp_setup.py`
2. Check Output panel for specific errors
3. Verify watsonx.ai service is up

---

## 💡 Pro Tips

### 1. Be Natural

Bob understands natural language:
```
Bob, check this file for bugs: mcp_server/server.py
```

### 2. Be Specific When Needed

For precise control, use explicit parameters:
```
Bob, use scan_code_quality to analyze mcp_server/server.py with scan_type "vulnerabilities" and auto_fix false
```

### 3. Chain Multiple Tasks

```
Bob, do this:
1. Scan dataset_balancia/src/app/actions/profileActions.ts for bugs
2. Generate documentation for it
3. Create unit tests
```

### 4. Use for Real Work

**Code Review:**
```
Bob, review my changes:
1. Check git diff
2. Scan modified files
3. Generate tests for new code
```

**Project Onboarding:**
```
Bob, help me understand this project:
1. Show project concept map
2. Show dependency chain
3. Document main modules
```

---

## 🎯 Quick Reference

### Basic Pattern

```
Bob, <action> <file/directory> [with <parameters>]
```

### Examples

```
Bob, scan mcp_server/server.py
Bob, document dataset_balancia/src/lib/utils.ts
Bob, create tests for mcp_server/watsonx_client.py
Bob, show architecture of dataset_balancia
```

---

## ✅ Summary

**DO:**
- ✅ Use IBM Bob chat interface
- ✅ Type natural language commands
- ✅ Use relative file paths
- ✅ Let Bob handle the MCP communication

**DON'T:**
- ❌ Create manual Python scripts
- ❌ Try to call the server directly
- ❌ Use absolute paths
- ❌ Bypass the MCP protocol

---

## 🚀 Ready to Use!

Your MCP server is configured and ready. Just:

1. **Open IBM Bob**
2. **Type a command** (e.g., `Bob, scan mcp_server/server.py`)
3. **Get results!**

**That's it! No scripts, no complexity, just chat!** 🎉

---

**Questions? Check:**
- [HOW_MCP_WORKS.md](HOW_MCP_WORKS.md) - Understanding MCP
- [TEAM_SETUP.md](TEAM_SETUP.md) - Team onboarding
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - All commands