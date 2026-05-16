"""
MCP Server Entry Point for IBM Bob Integration
Provides tools for code quality analysis and documentation generation, powered by IBM watsonx.ai
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry
from lib.doc_engine import DocEngine
from lib.ideation import IdeationEngine


class BobSuiteMCPServer:
    """Main MCP Server class integrating all BobSuite tools"""
    
    def __init__(self):
        self.server = Server("bobsuite-mcp")
        self.watsonx = WatsonxClient()
        self.qa_sentry = QASentry(self.watsonx)
        self.doc_engine = DocEngine(self.watsonx)
        self.ideation_engine = IdeationEngine(self.watsonx)
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all MCP tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools"""
            return [
                Tool(
                    name="scan_code_quality",
                    description="Analyze code for bugs, vulnerabilities, and quality issues using watsonx.ai with multi-agent verification (Finder vs Critic debate pattern)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the code file to analyze"
                            },
                            "scan_type": {
                                "type": "string",
                                "enum": ["bugs", "vulnerabilities", "quality", "all"],
                                "description": "Type of scan to perform",
                                "default": "all"
                            },
                            "auto_fix": {
                                "type": "boolean",
                                "description": "Automatically apply suggested fixes to the file (creates backup)",
                                "default": False
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="generate_documentation",
                    description="Generate comprehensive documentation for code using watsonx.ai",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the code file to document"
                            },
                            "doc_type": {
                                "type": "string",
                                "enum": ["inline", "api", "readme", "full"],
                                "description": "Type of documentation to generate"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="scan_git_diff",
                    description="Scan only changed lines from git diff (staged or working directory changes)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the git repository"
                            },
                            "staged": {
                                "type": "boolean",
                                "description": "If true, scan staged changes; if false, scan working directory changes",
                                "default": True
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                Tool(
                    name="get_project_framework",
                    description="Retrieve the 7-pillar ideation framework for structured feature planning. Use this to guide developers through creating comprehensive PRDs.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_examples": {
                                "type": "boolean",
                                "description": "Include example answers for each pillar to guide the developer",
                                "default": True
                            }
                        }
                    }
                ),
                Tool(
                    name="synthesize_project_plan",
                    description="Generate a comprehensive Product Requirements Document (PRD) from conversation data. Call this after completing the ideation interview.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "conversation_data": {
                                "type": "object",
                                "description": "Structured conversation data with pillar responses or full transcript"
                            },
                            "project_name": {
                                "type": "string",
                                "description": "Name of the project or feature being planned"
                            },
                            "output_path": {
                                "type": "string",
                                "description": "Optional custom path to save the PRD file. If not provided, AI will determine an appropriate location."
                            }
                        },
                        "required": ["conversation_data"]
                    }
                ),
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls with comprehensive error handling"""
            
            try:
                if name == "scan_code_quality":
                    # Extract parameters with defaults
                    file_path = arguments.get("file_path")
                    scan_type = arguments.get("scan_type", "all")
                    auto_fix = arguments.get("auto_fix", False)
                    
                    # Validate required parameters
                    if not file_path:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "success": False,
                                "error": "file_path parameter is required"
                            }, indent=2)
                        )]
                    
                    # Execute scan with all parameters
                    result = await self.qa_sentry.scan_code(
                        file_path=file_path,
                        scan_type=scan_type,
                        auto_fix=auto_fix
                    )
                    
                    # Generate the rich paragraphical markdown report
                    report_markdown = self.qa_sentry.generate_report([result])
                    return [TextContent(type="text", text=report_markdown)]
                
                elif name == "generate_documentation":
                    file_path = arguments.get("file_path")
                    doc_type = arguments.get("doc_type", "full")
                    
                    if not file_path:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "success": False,
                                "error": "file_path parameter is required"
                            }, indent=2)
                        )]
                    
                    result = await self.doc_engine.generate_docs(file_path, doc_type)
                    return [TextContent(type="text", text=result)]
                
                elif name == "scan_git_diff":
                    repo_path = arguments.get("repo_path")
                    staged = arguments.get("staged", True)
                    
                    if not repo_path:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "success": False,
                                "error": "repo_path parameter is required"
                            }, indent=2)
                        )]
                    
                    result = await self.qa_sentry.scan_git_diff(
                        repo_path=repo_path,
                        staged=staged
                    )
                    
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
                
                elif name == "get_project_framework":
                    include_examples = arguments.get("include_examples", True)
                    
                    # Get the framework structure
                    framework = self.ideation_engine.get_framework(include_examples=include_examples)
                    
                    # Format it nicely for Bob to use
                    formatted_framework = self.ideation_engine.format_framework_for_display()
                    
                    return [TextContent(type="text", text=formatted_framework)]
                
                elif name == "synthesize_project_plan":
                    conversation_data = arguments.get("conversation_data")
                    project_name = arguments.get("project_name")
                    output_path = arguments.get("output_path")
                    
                    if not conversation_data:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "success": False,
                                "error": "conversation_data parameter is required"
                            }, indent=2)
                        )]
                    
                    # Generate the PRD
                    result = await self.ideation_engine.synthesize_prd(
                        conversation_data=conversation_data,
                        project_name=project_name,
                        output_path=output_path
                    )
                    
                    if result.get("success"):
                        # Return the PRD markdown with metadata
                        response_text = f"{result['prd_markdown']}\n\n---\n\n"
                        response_text += f"**Generated:** {result['metadata']['generated_at']}\n"
                        if result.get('file_path'):
                            response_text += f"**Saved to:** `{result['file_path']}`\n"
                        
                        return [TextContent(type="text", text=response_text)]
                    else:
                        # Return error information
                        return [TextContent(type="text", text=json.dumps(result, indent=2))]
                
                else:
                    error_response = {
                        "success": False,
                        "error": f"Unknown tool: {name}",
                        "available_tools": [
                            "scan_code_quality",
                            "generate_documentation",
                            "scan_git_diff",
                            "get_project_framework",
                            "synthesize_project_plan"
                        ]
                    }
                    return [TextContent(type="text", text=json.dumps(error_response, indent=2))]
                    
            except Exception as e:
                # Comprehensive error handling - return structured JSON
                error_response = {
                    "success": False,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "tool_name": name,
                    "arguments": arguments
                }
                return [TextContent(type="text", text=json.dumps(error_response, indent=2))]
    
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

# Made with Bob
