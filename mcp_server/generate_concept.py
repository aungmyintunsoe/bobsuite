"""
Quick script to generate project concept map for mcp_server
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.visualizer import VisualizerEngine


async def main():
    print("Generating project concept map for mcp_server...")
    
    watsonx = WatsonxClient()
    visualizer = VisualizerEngine(watsonx)
    
    project_path = str(Path(__file__).parent)
    output_path = Path(__file__).parent / "test_outputs"
    output_path.mkdir(exist_ok=True)
    
    result = await visualizer.generate_project_concept(
        project_path=project_path,
        output_path=str(output_path)
    )
    
    if result.get("success"):
        print(f"Success! Project concept map generated")
        print(f"  Components identified: {result.get('components', 0)}")
        print(f"  Saved to: {result.get('saved_to')}")
        print(f"\nPreview:\n{result.get('markdown', '')[:500]}...")
    else:
        print(f"Failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
