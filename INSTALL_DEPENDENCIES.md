# Installing Python Dependencies

## ⚠️ Important: Python Not Found

The import errors you're seeing are because **Python is not installed or not in your PATH**.

## 🔍 Current Issue

```
Python was not found; run without arguments to install from the Microsoft Store
```

This means:
1. Python is not installed on your system, OR
2. Python is installed but not added to your PATH environment variable

## 📥 Solution: Install Python

### Option 1: Install from Python.org (Recommended)

1. **Download Python 3.11 or 3.12:**
   - Go to https://www.python.org/downloads/
   - Download the latest Python 3.11 or 3.12 installer for Windows

2. **Install Python:**
   - Run the installer
   - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation
   - Click "Install Now"

3. **Verify Installation:**
   ```powershell
   python --version
   # Should show: Python 3.11.x or 3.12.x
   ```

### Option 2: Install from Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Get" to install
4. Verify: `python --version`

## 📦 After Python is Installed

Once Python is installed, run these commands:

```powershell
# Navigate to mcp_server directory
cd d:\ibmbobhack\mcp_server

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## ✅ Verify Installation

After installing dependencies, verify each package:

```powershell
# Check if packages are installed
python -c "import mcp; print('✓ mcp installed')"
python -c "import dotenv; print('✓ python-dotenv installed')"
python -c "import httpx; print('✓ httpx installed')"
python -c "import ibm_watsonx_ai; print('✓ ibm-watsonx-ai installed')"
```

## 🎯 Expected Output After Installation

All import errors will disappear:
- ✓ `import mcp` - works
- ✓ `import dotenv` - works
- ✓ `import httpx` - works
- ✓ `import ibm_watsonx_ai` - works

## 🐛 Troubleshooting

### "python is not recognized"
- Python is not in PATH
- Reinstall Python and check "Add to PATH"
- Or manually add Python to PATH

### "pip is not recognized"
- Run: `python -m pip install --upgrade pip`

### "Cannot activate virtual environment"
- PowerShell execution policy issue
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### "Module not found after pip install"
- Make sure virtual environment is activated
- Look for `(venv)` at the start of your command prompt
- If not there, run: `.\venv\Scripts\Activate.ps1`

## 📝 Quick Reference

```powershell
# Full installation sequence (after Python is installed)
cd d:\ibmbobhack\mcp_server
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test_watsonx.py
```

## 🔗 Helpful Links

- Python Downloads: https://www.python.org/downloads/
- Python on Windows: https://docs.python.org/3/using/windows.html
- pip Documentation: https://pip.pypa.io/en/stable/
- Virtual Environments: https://docs.python.org/3/tutorial/venv.html

---

**Note:** The import errors in your IDE are **NORMAL** until you:
1. Install Python
2. Create a virtual environment
3. Install the dependencies with pip

Once these steps are complete, all red squiggly lines will disappear! ✨