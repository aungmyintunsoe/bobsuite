# BobSuite MCP

An AI-powered development toolkit for IBM Bob that provides enterprise-grade code analysis, automated documentation, and visual architecture mapping using IBM watsonx.ai.

## 🚀 Quick Start

### 1. Prerequisites
- **Python**: 3.8 or higher
- **IDE**: IBM Bob
- **IBM Cloud**: watsonx.ai access

### 2. Dependencies
Ensure you install the dependencies listed in `mcp_server/requirements.txt`:
- `python-dotenv>=1.0.0`
- `mcp>=0.9.0`
- `httpx>=0.24.0`
- `requests>=2.31.0`
- `pytest>=7.0.0` (for testing)
- `pytest-asyncio>=0.21.0` (for testing)

### 3. Setup & Installation
```bash
# Clone the repository
git clone https://github.com/your-org/bobsuite.git
cd bobsuite/mcp_server

# Create and activate a virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your IBM_API_KEY and PROJECT_ID
```

### 4. Integration with IBM Bob
Add BobSuite to your IBM Bob MCP settings (located at `~/.bob/mcp_settings.json`):

```json
{
  "mcpServers": {
    "bobsuite": {
      "command": "python",
      "args": ["/absolute/path/to/bobsuite/mcp_server/server.py"],
      "env": {
        "IBM_API_KEY": "your_api_key",
        "PROJECT_ID": "your_project_id"
      }
    }
  }
}
```

## 🛠️ Usage Examples

Once integrated, use natural language prompts directly in IBM Bob to leverage the AI engines:

- **Scan Code Quality**: 
  `Bob, scan dataset_balancia/src/app/actions.ts for all issues and generate tests`
- **Generate Documentation**: 
  `Bob, generate full documentation for mcp_server/lib/qa_sentry/`
- **Visualize Architecture**: 
  `Bob, generate a dependency chain for mcp_server with external dependencies`
- **Create a PRD**: 
  `Bob, generate a PRD from our conversation about the authentication feature`

## 🧠 Core Features

1. **QA Sentry**: Multi-agent code analysis (Finder vs. Critic) that discovers vulnerabilities, auto-fixes issues, and generates test cases.
2. **AutoDocs**: Generates 12 types of documentation concurrently (API, tutorials, user manuals).
3. **Visualizer**: Auto-generates Mermaid architecture diagrams (dependency chains, feature flows).
4. **Ideation**: Synthesizes structured Product Requirement Documents (PRDs) directly from your conversational prompts.

## 🧪 Testing

Run the test suite to verify the installation:
```bash
# Make sure you are in the mcp_server directory and your virtual environment is active
pytest tests/ -v
```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.