"""
Response Formatters
Handles formatting of various tool responses for MCP server
"""

from typing import Dict, Any, List
from mcp.types import TextContent


def format_test_generation_response(result: Dict[str, Any], test_type: str) -> str:
    """
    Unified formatter for test generation responses (network and unit tests).
    
    Args:
        result: Test generation result dictionary
        test_type: Type of test ('network' or 'unit')
        
    Returns:
        Formatted markdown string
    """
    # Title varies by test type
    title_map = {
        'network': 'Network Performance Tests Generated',
        'unit': 'Unit Tests Generated (Steve Sanderson Principles)'
    }
    
    response_parts = [
        f"# {title_map.get(test_type, 'Tests Generated')}",
        f"\n**File:** `{result['file_path']}`",
        f"\n**Language:** {result['language']}",
        f"\n**Test Framework:** {result['test_framework']}",
        f"\n**Timestamp:** {result['timestamp']}",
        f"\n\n## Framework Justification",
        f"\n{result['framework_justification']}",
        f"\n\n## Dependencies",
        "\n```bash"
    ]
    
    # Dependencies
    for dep in result.get('dependencies', []):
        response_parts.append(f"\n{dep}")
    response_parts.append("\n```")
    
    # Setup commands
    if result.get('setup_commands'):
        response_parts.append("\n\n## Setup Commands")
        response_parts.append("\n```bash")
        for cmd in result['setup_commands']:
            response_parts.append(f"\n{cmd}")
        response_parts.append("\n```")
    
    # Test files
    response_parts.append("\n\n## Test Files")
    for test_file in result.get('test_files', []):
        response_parts.append(f"\n\n### {test_file['filename']}")
        response_parts.append(f"\n{test_file['description']}")
        response_parts.append(f"\n\n```{result['language']}")
        response_parts.append(f"\n{test_file['content']}")
        response_parts.append("\n```")
    
    # Configuration files
    if result.get('configuration_files'):
        response_parts.append("\n\n## Configuration Files")
        for config_file in result['configuration_files']:
            response_parts.append(f"\n\n### {config_file['filename']}")
            response_parts.append(f"\n{config_file['description']}")
            response_parts.append(f"\n\n```{result['language']}")
            response_parts.append(f"\n{config_file['content']}")
            response_parts.append("\n```")
    
    # Execution command
    response_parts.append("\n\n## Execution Command")
    response_parts.append(f"\n```bash\n{result['execution_command']}\n```")
    
    # Type-specific sections
    if test_type == 'network':
        _append_network_specific_sections(response_parts, result)
    elif test_type == 'unit':
        _append_unit_specific_sections(response_parts, result)
    
    # Notes (common to both)
    if result.get('notes'):
        response_parts.append(f"\n\n## Notes\n{result['notes']}")
    
    return "".join(response_parts)


def _append_network_specific_sections(response_parts: List[str], result: Dict[str, Any]) -> None:
    """Append network test specific sections to response."""
    if result.get('performance_thresholds'):
        response_parts.append("\n\n## Performance Thresholds")
        thresholds = result['performance_thresholds']
        response_parts.append(f"\n- **Response Time:** {thresholds.get('response_time_ms', 'N/A')} ms")
        response_parts.append(f"\n- **Throughput:** {thresholds.get('throughput_rps', 'N/A')} requests/sec")
        response_parts.append(f"\n- **Error Rate:** {thresholds.get('error_rate_percent', 'N/A')}%")
    
    if result.get('test_scenarios'):
        response_parts.append("\n\n## Test Scenarios")
        for scenario in result['test_scenarios']:
            response_parts.append(f"\n- {scenario}")


def _append_unit_specific_sections(response_parts: List[str], result: Dict[str, Any]) -> None:
    """Append unit test specific sections to response."""
    if result.get('mock_strategy'):
        response_parts.append("\n\n## Mock Strategy")
        mock_strat = result['mock_strategy']
        response_parts.append(f"\n**Mocking Library:** {mock_strat.get('mocking_library', 'N/A')}")
        if mock_strat.get('external_dependencies'):
            response_parts.append("\n\n**External Dependencies Mocked:**")
            for dep in mock_strat['external_dependencies']:
                response_parts.append(f"\n- {dep}")
        if mock_strat.get('mock_examples'):
            response_parts.append("\n\n**Mock Patterns:**")
            for example in mock_strat['mock_examples']:
                response_parts.append(f"\n- {example}")
    
    if result.get('test_coverage'):
        response_parts.append("\n\n## Test Coverage")
        coverage = result['test_coverage']
        response_parts.append(f"\n**Total Tests:** {coverage.get('test_count', 'N/A')}")
        if coverage.get('units_tested'):
            response_parts.append("\n\n**Units Tested:**")
            for unit in coverage['units_tested']:
                response_parts.append(f"\n- {unit}")
        if coverage.get('coverage_notes'):
            response_parts.append(f"\n\n{coverage['coverage_notes']}")
    
    if result.get('design_principles_applied'):
        response_parts.append("\n\n## Design Principles Applied")
        for principle in result['design_principles_applied']:
            response_parts.append(f"\n- {principle}")


def format_visualizer_result(result: Dict[str, Any]) -> str:
    """
    Format visualizer engine results for MCP response.
    
    Primary: Direct user to open saved .md file in VS Code Markdown Preview.
    Fallback: Include raw Mermaid code for inline AI rendering.
    
    Args:
        result: Visualizer result dictionary
        
    Returns:
        Formatted markdown string
    """
    diagram_type = result.get("diagram_type", "visualization").replace("_", " ").title()
    response = f"✅ **{diagram_type} generated successfully!**\n\n"

    # Include stats if available
    if stats := result.get("stats"):
        response += "### 📊 Stats\n\n"
        response += "| Metric | Value |\n|--------|-------|\n"
        for key, val in stats.items():
            label = key.replace("_", " ").title()
            response += f"| {label} | **{val}** |\n"
        response += "\n"
    elif features := result.get("features_analyzed"):
        response += f"**Features analyzed:** {features}\n\n"
    elif components := result.get("components"):
        response += f"**Components identified:** {components}\n\n"
    
    if saved_to := result.get("saved_to"):
        response += "---\n\n"
        response += "### 📂 View Your Diagram\n\n"
        response += f"**File saved to:** `{saved_to}`\n\n"
        response += "**To view the rendered diagram:**\n"
        response += "1. Open the file in VS Code\n"
        response += "2. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac) to open Markdown Preview\n"
        response += "3. The Mermaid diagram will render automatically\n\n"
        response += "> 💡 **First time?** You need to install the **[Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)** extension by Matt Bierner in VS Code for the diagrams to render.\n\n"
        
        # Fallback for file-saved mode
        response += "---\n\n"
        response += "<details>\n<summary>📋 Raw Mermaid (click to expand — fallback if file preview unavailable)</summary>\n\n"
        response += "⚠️ **AI INSTRUCTION:** Only render this Mermaid code block if the user explicitly asks for inline rendering or cannot open the saved file:\n\n"
        response += result.get("mermaid", "")
        response += "\n\n</details>"
    else:
        # If no file was saved, render the Mermaid block directly
        response += "⚠️ **AI INSTRUCTION:** Immediately render the following Mermaid code block in your response so the user can see the diagram natively:\n\n"
        response += result.get("mermaid", "")
    
    return response


# Made with Bob