"""
MCP Server Entry Point for IBM Bob Integration
Provides tools for code quality analysis and documentation generation, powered by IBM watsonx.ai
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry
from lib.autodocs import AutoDocs
from lib.ideation import IdeationEngine
from lib.visualizer import VisualizerEngine


class BobSuiteMCPServer:
    """Main MCP Server class integrating all BobSuite tools"""
    
    def __init__(self):
        self.server = Server("bobsuite-mcp")
        self.watsonx = WatsonxClient()
        self.qa_sentry = QASentry(self.watsonx)
        self.autodocs = AutoDocs(self.watsonx)
        self.ideation_engine = IdeationEngine(self.watsonx)
        self.visualizer = VisualizerEngine(self.watsonx)
        
        self._register_handlers()

    # ------------------------------------------------------------------ #
    #                      HELPER METHODS                                #
    # ------------------------------------------------------------------ #

    def _error_response(self, error_msg: str, **kwargs) -> List[TextContent]:
        """Standardize error JSON outputs."""
        payload = {"success": False, "error": error_msg}
        payload.update(kwargs)
        return [TextContent(type="text", text=json.dumps(payload, indent=2))]

    def _success_response(self, text: str) -> List[TextContent]:
        """Standardize successful text/markdown outputs."""
        return [TextContent(type="text", text=text)]

    def _require_args(self, args: Dict[str, Any], required_keys: List[str]) -> Optional[List[TextContent]]:
        """Check for missing parameters and return an error response if any are missing."""
        for key in required_keys:
            if not args.get(key):
                return self._error_response(f"'{key}' parameter is required")
        return None

    def _format_visualizer_result(self, result: Dict[str, Any]) -> List[TextContent]:
        """Handle standardized output for all visualizer engine tools."""
        if not result.get("success"):
            return self._error_response(result.get("error", "Unknown visualizer error"))
        
        response = result["markdown"]
        
        if saved_to := result.get("saved_to"):
            response += f"\n\n✅ **Blueprint saved to:** `{saved_to}`"
            
        # Add this logic to announce the image file!
        if image_saved_to := result.get("image_saved_to"):
            response += f"\n🖼️ **Real Image saved to:** `{image_saved_to}`"
            
        return self._success_response(response)
    

    # ------------------------------------------------------------------ #
    #                      TOOL HANDLERS                                 #
    # ------------------------------------------------------------------ #

    async def _handle_scan_code_quality(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["file_path"]): return err
        
        result = await self.qa_sentry.scan_code(
            file_path=args["file_path"],
            scan_type=args.get("scan_type", "all"),
            auto_fix=args.get("auto_fix", False),
            additional_context=args.get("additional_context")
        )
        return self._success_response(self.qa_sentry.generate_report([result]))

    async def _handle_generate_docs(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["file_path"]): return err
        
        result = await self.autodocs.generate_docs(
            args["file_path"],
            args.get("doc_type", "full")
        )
        return self._success_response(result)

    async def _handle_scan_git_diff(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["repo_path"]): return err
        
        result = await self.qa_sentry.scan_git_diff(
            repo_path=args["repo_path"],
            staged=args.get("staged", True)
        )
        return self._success_response(json.dumps(result, indent=2))

    async def _handle_get_framework(self, args: Dict[str, Any]) -> List[TextContent]:
        self.ideation_engine.get_framework(include_examples=args.get("include_examples", True))
        return self._success_response(self.ideation_engine.format_framework_for_display())

    async def _handle_synthesize_plan(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["conversation_data"]): return err
        
        result = await self.ideation_engine.synthesize_prd(
            conversation_data=args["conversation_data"],
            project_name=args.get("project_name"),
            output_path=args.get("output_path")
        )
        
        if not result.get("success"):
            return self._success_response(json.dumps(result, indent=2))
            
        text = f"{result['prd_markdown']}\n\n---\n\n**Generated:** {result['metadata']['generated_at']}\n"
        if file_path := result.get('file_path'):
            text += f"**Saved to:** `{file_path}`\n"
            
        return self._success_response(text)

    async def _handle_dependency_chain(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["project_path"]): return err
        result = await self.visualizer.generate_dependency_chain(
            project_path=args["project_path"],
            output_path=args.get("output_path"),
            max_depth=args.get("max_depth", 3),
            include_external=args.get("include_external", False)
        )
        return self._format_visualizer_result(result)

    async def _handle_feature_flow(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["project_path"]): return err
        result = await self.visualizer.generate_feature_flow(
            project_path=args["project_path"],
            feature_name=args.get("feature_name"),
            output_path=args.get("output_path")
        )
        return self._format_visualizer_result(result)

    async def _handle_project_concept(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["project_path"]): return err
        result = await self.visualizer.generate_project_concept(
            project_path=args["project_path"],
            output_path=args.get("output_path")
        )
        return self._format_visualizer_result(result)

    async def _handle_generate_network_tests(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["file_path"]): return err
        
        result = await self.qa_sentry.generate_network_performance_tests(
            file_path=args["file_path"],
            testing_library=args.get("testing_library"),
            test_requirements=args.get("test_requirements")
        )
        
        if not result.get("success"):
            return self._error_response(result.get("error", "Unknown error"))
        
        # Format the response
        response_parts = [
            f"# Network Performance Tests Generated",
            f"\n**File:** `{result['file_path']}`",
            f"\n**Language:** {result['language']}",
            f"\n**Test Framework:** {result['test_framework']}",
            f"\n**Timestamp:** {result['timestamp']}",
            f"\n\n## Framework Justification",
            f"\n{result['framework_justification']}",
            f"\n\n## Dependencies",
            "\n```bash"
        ]
        
        for dep in result.get('dependencies', []):
            response_parts.append(f"\n{dep}")
        response_parts.append("\n```")
        
        if result.get('setup_commands'):
            response_parts.append("\n\n## Setup Commands")
            response_parts.append("\n```bash")
            for cmd in result['setup_commands']:
                response_parts.append(f"\n{cmd}")
            response_parts.append("\n```")
        
        response_parts.append("\n\n## Test Files")
        for test_file in result.get('test_files', []):
            response_parts.append(f"\n\n### {test_file['filename']}")
            response_parts.append(f"\n{test_file['description']}")
            response_parts.append(f"\n\n```{result['language']}")
            response_parts.append(f"\n{test_file['content']}")
            response_parts.append("\n```")
        
        if result.get('configuration_files'):
            response_parts.append("\n\n## Configuration Files")
            for config_file in result['configuration_files']:
                response_parts.append(f"\n\n### {config_file['filename']}")
                response_parts.append(f"\n{config_file['description']}")
                response_parts.append(f"\n\n```{result['language']}")
                response_parts.append(f"\n{config_file['content']}")
                response_parts.append("\n```")
        
        response_parts.append("\n\n## Execution Command")
        response_parts.append(f"\n```bash\n{result['execution_command']}\n```")
        
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
        
        if result.get('notes'):
            response_parts.append(f"\n\n## Notes\n{result['notes']}")
        
        return self._success_response("".join(response_parts))

    async def _handle_generate_unit_tests(self, args: Dict[str, Any]) -> List[TextContent]:
        if err := self._require_args(args, ["file_path"]): return err
        
        result = await self.qa_sentry.generate_unit_tests(
            file_path=args["file_path"],
            testing_library=args.get("testing_library"),
            test_requirements=args.get("test_requirements")
        )
        
        if not result.get("success"):
            return self._error_response(result.get("error", "Unknown error"))
        
        # Format the response
        response_parts = [
            f"# Unit Tests Generated (Steve Sanderson Principles)",
            f"\n**File:** `{result['file_path']}`",
            f"\n**Language:** {result['language']}",
            f"\n**Test Framework:** {result['test_framework']}",
            f"\n**Timestamp:** {result['timestamp']}",
            f"\n\n## Framework Justification",
            f"\n{result['framework_justification']}",
            f"\n\n## Dependencies",
            "\n```bash"
        ]
        
        for dep in result.get('dependencies', []):
            response_parts.append(f"\n{dep}")
        response_parts.append("\n```")
        
        if result.get('setup_commands'):
            response_parts.append("\n\n## Setup Commands")
            response_parts.append("\n```bash")
            for cmd in result['setup_commands']:
                response_parts.append(f"\n{cmd}")
            response_parts.append("\n```")
        
        response_parts.append("\n\n## Test Files")
        for test_file in result.get('test_files', []):
            response_parts.append(f"\n\n### {test_file['filename']}")
            response_parts.append(f"\n{test_file['description']}")
            response_parts.append(f"\n\n```{result['language']}")
            response_parts.append(f"\n{test_file['content']}")
            response_parts.append("\n```")
        
        if result.get('configuration_files'):
            response_parts.append("\n\n## Configuration Files")
            for config_file in result['configuration_files']:
                response_parts.append(f"\n\n### {config_file['filename']}")
                response_parts.append(f"\n{config_file['description']}")
                response_parts.append(f"\n\n```{result['language']}")
                response_parts.append(f"\n{config_file['content']}")
                response_parts.append("\n```")
        
        response_parts.append("\n\n## Execution Command")
        response_parts.append(f"\n```bash\n{result['execution_command']}\n```")
        
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
        
        if result.get('notes'):
            response_parts.append(f"\n\n## Notes\n{result['notes']}")
        
        return self._success_response("".join(response_parts))

    # ------------------------------------------------------------------ #
    #                      MCP REGISTRATION                              #
    # ------------------------------------------------------------------ #

    def _register_handlers(self):
        """Register all MCP tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            # Kept your original Tool definitions schema identically here to prevent breaking changes.
            return [
                Tool(
                    name="scan_code_quality",
                    description="Analyze code for bugs, vulnerabilities, and quality issues using watsonx.ai. Exposes optional additional_context for feeding live web searches or CVE documentation.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string"},
                            "scan_type": {"type": "string", "enum": ["bugs", "vulnerabilities", "quality", "all"], "default": "all"},
                            "auto_fix": {"type": "boolean", "default": False},
                            "additional_context": {
                                "type": "string",
                                "description": "Optional external context. You (IBM Bob) should run web searches for known vulnerabilities of third-party libraries imported in this file, and supply those findings here."
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="generate_documentation",
                    description="Generate comprehensive documentation for code using watsonx.ai. Supports 12 documentation types including user manuals, tutorials, API docs, and more.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the code file to document"},
                            "doc_type": {
                                "type": "string",
                                "enum": ["user_manual", "how_to_guide", "quick_start", "tutorial", "troubleshooting", "user_persona", "knowledge_base", "ux_design", "wireframe", "requirements", "api", "full"],
                                "default": "full",
                                "description": "Type of documentation to generate"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="scan_git_diff",
                    description="Scan only changed lines from git diff",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {"type": "string"},
                            "staged": {"type": "boolean", "default": True}
                        },
                        "required": ["repo_path"]
                    }
                ),
                Tool(
                    name="get_project_framework",
                    description="Retrieve the 7-pillar ideation framework for structured feature planning.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_examples": {"type": "boolean", "default": True}
                        }
                    }
                ),
                Tool(
                    name="synthesize_project_plan",
                    description="Generate a comprehensive PRD from conversation data.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "conversation_data": {"type": "object"},
                            "project_name": {"type": "string"},
                            "output_path": {"type": "string"}
                        },
                        "required": ["conversation_data"]
                    }
                ),
                Tool(
                    name="generate_dependency_chain",
                    description="Generate a visual dependency chain diagram.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "output_path": {"type": "string"},
                            "max_depth": {"type": "integer", "default": 3},
                            "include_external": {"type": "boolean", "default": False}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="generate_feature_flow",
                    description="Generate a visual feature flow map showing user journeys.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "feature_name": {"type": "string"},
                            "output_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="generate_project_concept",
                    description="Generate a high-level project concept map.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "output_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="generate_network_performance_tests",
                    description="Generate comprehensive network performance tests for API endpoints and network calls. Bob autonomously selects the best testing framework or uses the one you specify (Jest, Postman/Newman, Pytest, Artillery, k6, etc.).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the code file containing API/network code"
                            },
                            "testing_library": {
                                "type": "string",
                                "description": "Optional: Specific testing library to use (e.g., 'jest', 'postman', 'pytest', 'artillery', 'k6'). If not specified, Bob will autonomously select the best one."
                            },
                            "test_requirements": {
                                "type": "string",
                                "description": "Optional: Specific requirements or scenarios to test (e.g., 'test rate limiting', 'concurrent requests', 'timeout handling')"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="generate_unit_tests",
                    description="Generate comprehensive unit tests following Steve Sanderson principles (S/S/R naming, isolation, mocking, single assertions). Bob autonomously selects the best testing framework or uses the one you specify (Jest, Pytest, JUnit, NUnit, etc.).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the code file to generate unit tests for"
                            },
                            "testing_library": {
                                "type": "string",
                                "description": "Optional: Specific testing library to use (e.g., 'jest', 'pytest', 'junit', 'nunit'). If not specified, Bob will autonomously select the best one."
                            },
                            "test_requirements": {
                                "type": "string",
                                "description": "Optional: Specific requirements or focus areas for the tests"
                            }
                        },
                        "required": ["file_path"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls via a centralized dispatcher map"""
            
            # Map tools to their designated handler methods
            dispatcher = {
                "scan_code_quality": self._handle_scan_code_quality,
                "generate_documentation": self._handle_generate_docs,
                "scan_git_diff": self._handle_scan_git_diff,
                "get_project_framework": self._handle_get_framework,
                "synthesize_project_plan": self._handle_synthesize_plan,
                "generate_dependency_chain": self._handle_dependency_chain,
                "generate_feature_flow": self._handle_feature_flow,
                "generate_project_concept": self._handle_project_concept,
                "generate_network_performance_tests": self._handle_generate_network_tests,
                "generate_unit_tests": self._handle_generate_unit_tests
            }

            try:
                # Route the request
                if handler := dispatcher.get(name):
                    return await handler(arguments or {})
                else:
                    return self._error_response(f"Unknown tool: {name}", available_tools=list(dispatcher.keys()))
                    
            except Exception as e:
                return self._error_response(str(e), error_type=type(e).__name__, tool_name=name, arguments=arguments)

    async def run(self):
        """Start the MCP server"""
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = BobSuiteMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())