"""
Test Suite for Visualizer Engine
Tests dependency chain, feature flow, and project concept generation
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.visualizer import VisualizerEngine


def print_section(title: str):
    print(f"\n{'=' * 70}\n  {title}\n{'=' * 70}\n")

def print_result(test_name: str, success: bool, details: str = ""):
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"  → {details}")


async def test_dependency_chain(visualizer: VisualizerEngine, project_path: str, output_path: Path) -> bool:
    print_section("TEST 1: Dependency Chain Generation")
    try:
        print(f"Analyzing project: {project_path}")
        result = await visualizer.generate_dependency_chain(
            project_path=project_path,
            output_path=str(output_path),
            max_depth=2,
            include_external=True
        )
        
        if result.get("success"):
            print_result("Dependency chain generation", True)
            print(f"  → Total modules: {result['stats']['total_modules']}")
            print(f"  → Total dependencies: {result['stats']['total_dependencies']}")
            print(f"  → External deps: {result['stats']['external_deps']}")
            print_result("Mermaid diagram generated", "```mermaid" in result.get("markdown", ""))
            print_result("File save", True, f"Saved to {result.get('saved_to')}")
            return True
            
        print_result("Dependency chain generation", False, result.get("error", "Unknown error"))
        return False
    except Exception as e:
        print_result("Dependency chain generation", False, f"Exception: {str(e)}")
        return False


async def test_feature_flow(visualizer: VisualizerEngine, project_path: str, output_path: Path) -> bool:
    print_section("TEST 2: Feature Flow Generation")
    try:
        print(f"Analyzing project: {project_path}")
        print("Note: This test uses AI to analyze features, may take longer...")
        result = await visualizer.generate_feature_flow(
            project_path=project_path,
            output_path=str(output_path)
        )
        
        if result.get("success"):
            print_result("Feature flow generation", True)
            print(f"  → Features analyzed: {result.get('features_analyzed', 0)}")
            print_result("Mermaid sequence diagram generated", "```mermaid" in result.get("markdown", ""))
            print_result("File save", True, f"Saved to {result.get('saved_to')}")
            return True
            
        print_result("Feature flow generation", False, result.get("error", "Unknown error"))
        return False
    except Exception as e:
        print_result("Feature flow generation", False, f"Exception: {str(e)}")
        return False


async def test_project_concept(visualizer: VisualizerEngine, project_path: str, output_path: Path) -> bool:
    print_section("TEST 3: Project Concept Generation")
    try:
        print(f"Analyzing project: {project_path}")
        print("Note: This test uses AI to understand architecture, may take longer...")
        result = await visualizer.generate_project_concept(
            project_path=project_path,
            output_path=str(output_path)
        )
        
        if result.get("success"):
            print_result("Project concept generation", True)
            print(f"  → Components identified: {result.get('components', 0)}")
            print_result("Mermaid architecture diagram generated", "```mermaid" in result.get("markdown", ""))
            print_result("File save", True, f"Saved to {result.get('saved_to')}")
            return True
            
        print_result("Project concept generation", False, result.get("error", "Unknown error"))
        return False
    except Exception as e:
        print_result("Project concept generation", False, f"Exception: {str(e)}")
        return False


async def test_error_handling(visualizer: VisualizerEngine) -> bool:
    print_section("TEST 4: Error Handling")
    try:
        result = await visualizer.generate_dependency_chain(project_path="/nonexistent/path")
        
        if not result.get("success") and "does not exist" in result.get("error", "").lower():
            print_result("Invalid path handling", True, "Correctly rejected non-existent path")
            return True
            
        print_result("Invalid path handling", False, "Should have rejected invalid path")
        return False
    except Exception as e:
        print_result("Error handling", False, f"Exception: {str(e)}")
        return False


async def main():
    print("\n" + "=" * 70)
    print("  VISUALIZER ENGINE TEST SUITE")
    print("  Testing dependency chain, feature flow, and project concept generation")
    print("=" * 70)
    
    watsonx = WatsonxClient()
    visualizer = VisualizerEngine(watsonx)
    
    project_path = str(Path(__file__).parent)
    output_path = Path(__file__).parent / "test_outputs"
    output_path.mkdir(exist_ok=True)
    
    results = [
        await test_dependency_chain(visualizer, project_path, output_path),
        await test_feature_flow(visualizer, project_path, output_path),
        await test_project_concept(visualizer, project_path, output_path),
        await test_error_handling(visualizer)
    ]
    
    print_section("TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n✓ All tests passed! Visualizer is ready to use.")
        print("\nGenerated visualizations saved to: mcp_server/test_outputs/")
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please review the errors above.")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())