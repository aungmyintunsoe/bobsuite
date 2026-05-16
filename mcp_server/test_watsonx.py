"""
Test script for IBM watsonx.ai client
Run this to verify your credentials and connection are working
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry
from lib.doc_engine import DocEngine


async def test_connection():
    """Test basic connection to watsonx.ai"""
    print("=" * 60)
    print("Testing IBM watsonx.ai Connection")
    print("=" * 60)
    
    try:
        # Initialize client
        print("\n1. Initializing WatsonxClient...")
        client = WatsonxClient()
        print("   ✓ Client initialized successfully")
        print(f"   - API Key: {client.api_key[:10]}..." if client.api_key else "   - API Key: Not set")
        print(f"   - Project ID: {client.project_id}")
        print(f"   - URL: {client.watsonx_url}")
        
    except ValueError as e:
        print(f"   ✗ Configuration Error: {e}")
        print("\n   Please ensure your .env file contains:")
        print("   - IBM_API_KEY=your_api_key")
        print("   - PROJECT_ID=your_project_id")
        print("   - WATSONX_URL=https://us-south.ml.cloud.ibm.com")
        return False
    
    except ImportError as e:
        print(f"   ✗ Import Error: {e}")
        print("\n   Please install required packages:")
        print("   pip install ibm-watsonx-ai python-dotenv")
        return False
    
    except Exception as e:
        print(f"   ✗ Unexpected Error: {e}")
        return False
    
    # Test text generation
    try:
        print("\n2. Testing text generation...")
        prompt = "Say 'Hello from IBM watsonx.ai!' in a friendly way."
        
        response = await client.generate_text(
            prompt=prompt,
            max_tokens=50,
            temperature=0.7
        )
        
        print("   ✓ Text generation successful!")
        print(f"\n   Prompt: {prompt}")
        print(f"   Response: {response[:200]}..." if len(response) > 200 else f"   Response: {response}")
        
    except Exception as e:
        print(f"   ✗ Text Generation Error: {e}")
        print("\n   This could mean:")
        print("   - Invalid API credentials")
        print("   - Project ID doesn't have access to the model")
        print("   - Network connectivity issues")
        return False
    
    # Test code analysis
    try:
        print("\n3. Testing code analysis...")
        test_code = """
def calculate_sum(a, b):
    return a + b

result = calculate_sum(5, 10)
print(result)
"""
        qa = QASentry(client)
        prompt = qa._build_analysis_prompt(test_code, "quality", "Python")
        
        response = await client.generate_text(prompt, temperature=0.3)
        
        print("   ✓ Code analysis prompt & generation successful!")
        print(f"   Results Preview: {response[:150]}...")
        
    except Exception as e:
        print(f"   ✗ Code Analysis Error: {e}")
        return False
    
    # Test documentation generation
    try:
        print("\n4. Testing documentation generation...")
        
        doc = DocEngine(client)
        prompt = doc._build_documentation_prompt(test_code, "inline", "Python")
        
        response = await client.generate_text(prompt, temperature=0.5)
        
        print("   ✓ Documentation generation successful!")
        print(f"\n   Documentation Preview: {response[:150]}...")
        
    except Exception as e:
        print(f"   ✗ Documentation Generation Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All tests passed! Your watsonx.ai client is working correctly.")
    print("=" * 60)
    return True


async def test_available_models():
    """Test which models are available in your project"""
    print("\n" + "=" * 60)
    print("Checking Available Models")
    print("=" * 60)
    
    try:
        client = WatsonxClient()
        
        # Try different models
        models_to_test = [
            "ibm/granite-13b-chat-v2",
            "ibm/granite-13b-instruct-v2",
            "meta-llama/llama-2-70b-chat",
            "google/flan-ul2",
        ]
        
        print("\nTesting models (this may take a moment)...")
        
        for model_id in models_to_test:
            try:
                print(f"\n  Testing: {model_id}")
                response = await client.generate_text(
                    prompt="Hello",
                    model_id=model_id,
                    max_tokens=10
                )
                print(f"  ✓ {model_id} - Available")
            except Exception as e:
                print(f"  ✗ {model_id} - Not available or error: {str(e)[:50]}")
        
    except Exception as e:
        print(f"\n✗ Error checking models: {e}")


def main():
    """Main test runner"""
    print("\n🚀 IBM watsonx.ai Client Test Suite\n")
    
    # Run connection test
    success = asyncio.run(test_connection())
    
    if success:
        # Optionally test available models
        print("\n" + "=" * 60)
        response = input("Would you like to test available models? (y/n): ")
        if response.lower() == 'y':
            asyncio.run(test_available_models())
    
    print("\n✨ Test complete!\n")


if __name__ == "__main__":
    main()

# Made with Bob
