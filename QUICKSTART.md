# 🚀 BobSuite MCP Quick Start Guide

Get your MCP server running in 5 minutes!

## ⚡ Prerequisites

- Python 3.8 or higher
- IBM Cloud account with watsonx.ai access
- IBM Bob IDE installed
- Your IBM API credentials ready

## 📝 Step-by-Step Setup

### 1. Install Python Dependencies

```bash
cd mcp_server
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed ibm-watsonx-ai-X.X.X python-dotenv-X.X.X mcp-X.X.X
```

### 2. Configure Your Credentials

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Add your credentials:**
```env
IBM_API_KEY=your_actual_api_key_here
PROJECT_ID=your_actual_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Where to find these:**
- **IBM_API_KEY**: IBM Cloud → Manage → Access (IAM) → API keys
- **PROJECT_ID**: watsonx.ai → Projects → Your Project → Settings
- **WATSONX_URL**: Usually `https://us-south.ml.cloud.ibm.com` (or your region)

### 3. Test Your Connection

```bash
python test_watsonx.py
```

**Expected output:**
```
============================================================
Testing IBM watsonx.ai Connection
============================================================

1. Initializing WatsonxClient...
   ✓ Client initialized successfully
   - API Key: pak-xxxxx...
   - Project ID: your-project-id
   - URL: https://us-south.ml.cloud.ibm.com

2. Testing text generation...
   ✓ Text generation successful!
   
3. Testing code analysis...
   ✓ Code analysis successful!
   
4. Testing documentation generation...
   ✓ Documentation generation successful!

============================================================
✓ All tests passed! Your watsonx.ai client is working correctly.
============================================================
```

**If you see errors:**
- ❌ Configuration Error → Check your .env file
- ❌ Import Error → Run `pip install -r requirements.txt`
- ❌ API Error → Verify your API key and project ID

### 4. Add Test Data (Optional)

```bash
# Copy your Balancia project or create a test file
cd ../dataset_balancia

# Create a simple test file
echo "def hello(): print('Hello World')" > test.py
```

### 5. Configure IBM Bob

Open IBM Bob's MCP settings and add:

```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["d:/ibmbobhack/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "d:/ibmbobhack/mcp_server"
      }
    }
  }
}
```

**Adjust the path** to match your actual project location!

### 6. Test with IBM Bob

Restart IBM Bob, then try these commands:

**Test 1: Read a file**
```
Bob, use read_dataset_file to read "test.py"
```

**Test 2: Scan code quality**
```
Bob, use scan_code_quality to analyze dataset_balancia/test.py with scan_type "all"
```

**Test 3: Generate documentation**
```
Bob, use generate_documentation for dataset_balancia/test.py with doc_type "full"
```

## ✅ Success Checklist

- [ ] Python dependencies installed
- [ ] .env file configured with credentials
- [ ] test_watsonx.py runs successfully
- [ ] Test files added to dataset_balancia/
- [ ] IBM Bob MCP settings configured
- [ ] Tools work in IBM Bob

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Invalid credentials" error
1. Check your .env file exists in `mcp_server/`
2. Verify API key is correct (no extra spaces)
3. Verify project ID is correct
4. Try regenerating your API key in IBM Cloud

### "Model not found" error
1. Check your project has access to Granite models
2. Try a different model in watsonx_client.py:
   ```python
   model_id="ibm/granite-13b-instruct-v2"
   ```

### IBM Bob can't find the server
1. Check the path in MCP settings is correct
2. Make sure Python is in your PATH
3. Try absolute path to python.exe:
   ```json
   "command": "C:/Python39/python.exe"
   ```

### Server starts but tools don't work
1. Check server.py for syntax errors
2. Verify .env file is in mcp_server/ directory
3. Check logs in IBM Bob's output panel

## 📚 Next Steps

Once everything works:

1. **Add your real project** to `dataset_balancia/`
2. **Test all three tools** with your code
3. **Generate reports** and save to `bob_sessions/`
4. **Customize prompts** in `watsonx_client.py` if needed
5. **Add more tools** by extending `server.py`

## 🎯 Quick Commands Reference

```bash
# Activate environment
cd mcp_server
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Test connection
python test_watsonx.py

# Run server manually (for debugging)
python server.py

# Deactivate environment
deactivate
```

## 💡 Pro Tips

1. **Keep .env secure** - Never commit it to git (already in .gitignore)
2. **Test incrementally** - Test each component before moving to the next
3. **Check logs** - IBM Bob shows MCP server logs in the output panel
4. **Use test files** - Test with simple files before analyzing large projects
5. **Save sessions** - Export your Bob sessions to `bob_sessions/` for judging

## 🆘 Still Having Issues?

1. Read `mcp_server/ARCHITECTURE.md` for detailed explanations
2. Check the main `README.md` for more information
3. Verify your IBM Cloud account has watsonx.ai access
4. Make sure your project has the Granite models enabled

---

**Ready to go?** Start with Step 1 and work through each step carefully. Good luck with the hackathon! 🚀