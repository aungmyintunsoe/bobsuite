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
    Format visualizer engine results with markdown and file paths.
    
    Args:
        result: Visualizer result dictionary
        
    Returns:
        Formatted markdown string
    """
    response = "✅ **Visualization successfully generated!**\n"
    
    if saved_to := result.get("saved_to"):
        response += f"**Saved full markdown document to:** `{saved_to}`\n\n"
        
    response += "⚠️ **AI INSTRUCTION:** Immediately render the following Mermaid code block in your response so the user can see the diagram natively:\n\n"
    response += result.get("mermaid", "")
    
    return response


# Made with Bob