# 🚀 MCP Server Quick Reference Card

**Fast access to all commands and configurations**

---

## 🔧 Setup Commands

```bash
# Navigate to project
cd d:/bobsuite/mcp_server

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Test setup
python test_mcp_setup.py

# Start server manually (for debugging)
python server.py
```

---

## 🔌 IBM Bob MCP Configuration

**File location:** `%APPDATA%\Code\User\globalStorage\ibm.bob\settings.json`

**Configuration:**
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

**⚠️ Replace `d:/bobsuite` with your actual path!**

---

## 🧪 Test Commands for IBM Bob

### Critical Tools (Test First)

**1. Scan Code Quality**
```
Bob, use scan_code_quality to analyze mcp_server/server.py with scan_type "quality"
```

**2. Generate Documentation**
```
Bob, generate documentation for mcp_server/watsonx_client.py with doc_type "api"
```

### Important Tools

**3. Project Concept Map**
```
Bob, generate a project concept map for the mcp_server directory
```

**4. Dependency Chain**
```
Bob, generate a dependency chain for mcp_server with max_depth 2
```

**5. Unit Tests**
```
Bob, generate unit tests for mcp_server/watsonx_client.py
```

### Optional Tools

**6. Git Diff Analysis**
```
Bob, use scan_git_diff to analyze changes in d:/bobsuite with staged set to true
```

**7. Project Framework**
```
Bob, use get_project_framework with include_examples set to true
```

**8. Feature Flow**
```
Bob, generate a feature flow map for the mcp_server directory
```

**9. Project Plan**
```
Bob, use synthesize_project_plan with conversation_data containing a project idea
```

**10. Network Tests**
```
Bob, generate network performance tests for mcp_server/watsonx_client.py
```

---

## 📊 All 10 Available Tools

| # | Tool Name | Purpose | Priority |
|---|-----------|---------|----------|
| 1 | `scan_code_quality` | Bug/vulnerability detection | 🔴 Critical |
| 2 | `generate_documentation` | Auto-generate docs | 🔴 Critical |
| 3 | `generate_project_concept` | Architecture overview | 🟡 Important |
| 4 | `generate_dependency_chain` | Module relationships | 🟡 Important |
| 5 | `generate_unit_tests` | Test generation | 🟡 Important |
| 6 | `scan_git_diff` | Git change analysis | 🟢 Optional |
| 7 | `get_project_framework` | 7-pillar ideation | 🟢 Optional |
| 8 | `generate_feature_flow` | User journey maps | 🟢 Optional |
| 9 | `synthesize_project_plan` | PRD generation | 🟢 Optional |
| 10 | `generate_network_performance_tests` | API test generation | 🟢 Optional |

---

## 🐛 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Module not found | `pip install -r requirements.txt` |
| Invalid credentials | Check `.env` file in `mcp_server/` |
| Server won't start | Verify Python path in MCP settings |
| Tools not discovered | Check Output panel for errors |
| Slow responses | Check internet connection |
| Import errors | Run `python test_mcp_setup.py` |

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `mcp_server/server.py` | Main MCP server |
| `mcp_server/.env` | Your credentials (protected) |
| `mcp_server/.env.example` | Credential template |
| `mcp_server/test_mcp_setup.py` | Setup verification script |
| `STEP_BY_STEP_SETUP.md` | Complete setup guide |
| `mcp_server/MCP_SETUP_GUIDE.md` | Detailed documentation |
| `mcp_server/TESTING_PLAN.md` | Testing strategy |

---

## 🎯 Success Checklist

**Minimum (MVP):**
- [ ] Server connects to IBM Bob
- [ ] 2 critical tools work
- [ ] No connection errors

**Production Ready:**
- [ ] All 10 tools operational
- [ ] Response time <45s average
- [ ] Documentation complete

---

## 💡 Real-World Usage Examples

### Code Review
```
Bob, review my code:
1. Scan mcp_server/lib/qa_sentry/core.py for quality issues
2. Generate API documentation for it
3. Create unit tests
```

### Project Onboarding
```
Bob, help me understand this project:
1. Generate project concept map
2. Show dependency chain
3. Create feature flow diagram
```

### Documentation Sprint
```
Bob, document everything:
1. Generate docs for all files in mcp_server/lib/
2. Create comprehensive README
3. Add usage examples
```

---

## 🔗 Quick Links

- **Full Setup Guide:** [`STEP_BY_STEP_SETUP.md`](STEP_BY_STEP_SETUP.md)
- **Testing Plan:** [`mcp_server/TESTING_PLAN.md`](mcp_server/TESTING_PLAN.md)
- **Architecture:** [`mcp_server/reports/ARCHITECTURE.md`](mcp_server/reports/ARCHITECTURE.md)
- **Quick Start:** [`QUICKSTART.md`](QUICKSTART.md)

---

**Print this page and keep it handy! 📄**