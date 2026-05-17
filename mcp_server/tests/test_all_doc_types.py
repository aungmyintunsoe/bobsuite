"""
Test script to demonstrate all 12 documentation types in AutoDocs
Run this to see examples of each documentation type
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.autodocs import AutoDocs
from watsonx_client import WatsonxClient


# Sample code to document
SAMPLE_CODE = """
// Sample Balancia actions
export async function getBalance(userId: string): Promise<number> {
    const response = await fetch('/api/balance/' + userId);
    const data = await response.json();
    return data.balance;
}

export async function transferFunds(fromId: string, toId: string, amount: number): Promise<boolean> {
    const response = await fetch('/api/transfer', {
        method: 'POST',
        body: JSON.stringify({ fromId, toId, amount })
    });
    return response.ok;
}
"""


async def test_documentation_type(autodocs: AutoDocs, doc_type: str, doc_name: str):
    """Test a specific documentation type"""
    print(f"\n{'='*70}")
    print(f"GENERATING: {doc_name}")
    print(f"Type: {doc_type}")
    print(f"{'='*70}\n")
    
    # Create a temporary file with sample code
    temp_file = Path("temp_sample.ts")
    temp_file.write_text(SAMPLE_CODE)
    
    try:
        # Generate documentation
        docs = await autodocs.generate_docs(str(temp_file), doc_type)
        
        # Display preview
        lines = docs.split('\n')
        preview_lines = min(30, len(lines))
        print('\n'.join(lines[:preview_lines]))
        
        if len(lines) > preview_lines:
            print(f"\n... ({len(lines) - preview_lines} more lines)")
        
        # Save to file
        output_file = Path(f"output_{doc_type}.md")
        output_file.write_text(docs, encoding='utf-8')
        print(f"\n✓ Saved to: {output_file}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()


async def main():
    """Main test function"""
    print("="*70)
    print("AUTODOCS - 12 DOCUMENTATION TYPES DEMONSTRATION")
    print("="*70)
    
    # Initialize watsonx client
    print("\nInitializing WatsonX client...")
    watsonx = WatsonxClient()
    
    # Initialize AutoDocs
    autodocs = AutoDocs(watsonx)
    
    # All 12 documentation types
    doc_types = [
        ("user_manual", "User Manual"),
        ("how_to_guide", "How-To Guide"),
        ("quick_start", "Quick Start Guide"),
        ("tutorial", "Tutorial"),
        ("troubleshooting", "Troubleshooting Guide"),
        ("user_persona", "User Persona"),
        ("knowledge_base", "Knowledge Base Article"),
        ("ux_design", "UX Design Documentation"),
        ("wireframe", "Wireframe Documentation"),
        ("requirements", "Software Requirements Specification"),
        ("api", "API Documentation"),
        ("full", "Comprehensive Documentation (All Types)"),
    ]
    
    print(f"\nAvailable documentation types: {len(doc_types)}")
    print("\nGenerating documentation for each type...\n")
    
    # Test each documentation type
    for doc_type, doc_name in doc_types:
        await test_documentation_type(autodocs, doc_type, doc_name)
        await asyncio.sleep(1)  # Small delay between requests
    
    print("\n" + "="*70)
    print("DOCUMENTATION GENERATION COMPLETE")
    print("="*70)
    print("\nGenerated files:")
    for doc_type, _ in doc_types:
        output_file = Path(f"output_{doc_type}.md")
        if output_file.exists():
            print(f"  ✓ output_{doc_type}.md")
    
    print("\n" + "="*70)
    print("USAGE EXAMPLES:")
    print("="*70)
    print("""
To generate a specific documentation type, use:

    from lib.autodocs import AutoDocs
    from watsonx_client import WatsonxClient
    
    watsonx = WatsonxClient()
    autodocs = AutoDocs(watsonx)
    
    # Generate wireframe documentation
    docs = await autodocs.generate_docs("path/to/file.ts", "wireframe")
    
    # Generate user manual
    docs = await autodocs.generate_docs("path/to/file.py", "user_manual")
    
    # Generate quick start guide
    docs = await autodocs.generate_docs("path/to/file.js", "quick_start")

Available types:
  - user_manual: Comprehensive user manuals
  - how_to_guide: Step-by-step how-to guides
  - quick_start: Quick-start guides
  - tutorial: Interactive tutorials
  - troubleshooting: Troubleshooting guides
  - user_persona: User personas
  - knowledge_base: Internal knowledge base articles
  - ux_design: UX design documentation
  - wireframe: Wireframes and UI mockups
  - requirements: Software requirement specifications
  - api: API documentation
  - full: Comprehensive documentation (all types combined)
""")


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
