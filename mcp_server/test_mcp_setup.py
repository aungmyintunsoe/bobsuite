"""
Quick test script to verify MCP server setup
Run this before configuring IBM Bob to ensure everything works
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("=" * 60)
    print("STEP 1: Testing Module Imports")
    print("=" * 60)
    
    try:
        from watsonx_client import WatsonxClient
        print("[OK] WatsonxClient imported")
    except Exception as e:
        print(f"[FAIL] WatsonxClient import failed: {e}")
        return False
    
    try:
        from lib.qa_sentry import QASentry
        print("[OK] QASentry imported")
    except Exception as e:
        print(f"[FAIL] QASentry import failed: {e}")
        return False
    
    try:
        from lib.autodocs import AutoDocs
        print("[OK] AutoDocs imported")
    except Exception as e:
        print(f"[FAIL] AutoDocs import failed: {e}")
        return False
    
    try:
        from lib.ideation import IdeationEngine
        print("[OK] IdeationEngine imported")
    except Exception as e:
        print(f"[FAIL] IdeationEngine import failed: {e}")
        return False
    
    try:
        from lib.visualizer import VisualizerEngine
        print("[OK] VisualizerEngine imported")
    except Exception as e:
        print(f"[FAIL] VisualizerEngine import failed: {e}")
        return False
    
    try:
        from mcp.server import Server
        print("[OK] MCP Server imported")
    except Exception as e:
        print(f"[FAIL] MCP Server import failed: {e}")
        return False
    
    print("\n[OK] All imports successful!\n")
    return True

async def test_watsonx_connection():
    """Test connection to IBM watsonx.ai"""
    print("=" * 60)
    print("STEP 2: Testing Watsonx Connection")
    print("=" * 60)
    
    try:
        from watsonx_client import WatsonxClient
        client = WatsonxClient()
        
        print(f"[OK] WatsonxClient initialized")
        print(f"  API Key: {client.api_key[:15]}..." if client.api_key else "  API Key: NOT SET")
        print(f"  Project ID: {client.project_id}")
        print(f"  URL: {client.watsonx_url}")
        
        # Try to get a token
        try:
            token = await client._get_token()
            print(f"[OK] Successfully obtained access token")
            print(f"  Token: {token[:20]}...")
        except Exception as e:
            print(f"[FAIL] Failed to get access token: {e}")
            return False
        
        print("\n[OK] Watsonx connection successful!\n")
        return True
        
    except Exception as e:
        print(f"[FAIL] Watsonx connection failed: {e}")
        return False

async def test_module_initialization():
    """Test that all modules can be initialized"""
    print("=" * 60)
    print("STEP 3: Testing Module Initialization")
    print("=" * 60)
    
    try:
        from watsonx_client import WatsonxClient
        from lib.qa_sentry import QASentry
        from lib.autodocs import AutoDocs
        from lib.ideation import IdeationEngine
        from lib.visualizer import VisualizerEngine
        
        client = WatsonxClient()
        
        qa = QASentry(client)
        print("[OK] QASentry initialized")
        
        docs = AutoDocs(client)
        print("[OK] AutoDocs initialized")
        
        ideation = IdeationEngine(client)
        print("[OK] IdeationEngine initialized")
        
        viz = VisualizerEngine(client)
        print("[OK] VisualizerEngine initialized")
        
        print("\n[OK] All modules initialized successfully!\n")
        return True
        
    except Exception as e:
        print(f"[FAIL] Module initialization failed: {e}")
        return False

def test_mcp_server():
    """Test that MCP server can be imported and initialized"""
    print("=" * 60)
    print("STEP 4: Testing MCP Server")
    print("=" * 60)
    
    try:
        from server import BobSuiteMCPServer
        
        server = BobSuiteMCPServer()
        print("[OK] BobSuiteMCPServer initialized")
        print(f"  Server name: {server.server.name}")
        print(f"  Tools registered: 10 expected")
        
        print("\n[OK] MCP Server ready!\n")
        return True
        
    except Exception as e:
        print(f"[FAIL] MCP Server initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MCP SERVER SETUP TEST")
    print("=" * 60 + "\n")
    
    # Test 1: Imports
    if not test_imports():
        print("\n[FAILED] Module imports failed")
        print("   Solution: Run 'pip install -r requirements.txt'")
        return False
    
    # Test 2: Watsonx connection
    if not await test_watsonx_connection():
        print("\n[FAILED] Watsonx connection failed")
        print("   Solution: Check your .env file has correct credentials")
        return False
    
    # Test 3: Module initialization
    if not await test_module_initialization():
        print("\n[FAILED] Module initialization failed")
        return False
    
    # Test 4: MCP Server
    if not test_mcp_server():
        print("\n[FAILED] MCP Server initialization failed")
        return False
    
    # All tests passed
    print("=" * 60)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYour MCP server is ready to use with IBM Bob!")
    print("\nNext steps:")
    print("1. Configure IBM Bob MCP settings (see STEP_BY_STEP_SETUP.md)")
    print("2. Restart IBM Bob")
    print("3. Test tools in IBM Bob chat")
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

# Made with Bob
