"""
MCP Server Entry Point for IBM Bob Integration
Provides tools for code quality analysis, documentation generation, and file management
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
from lib.file_manager import FileManager


class BobSuiteMCPServer:
    """Main MCP Server class integrating all BobSuite tools"""
    
    def __init__(self):
        self.server = Server("bobsuite-mcp")
        self.watsonx = WatsonxClient()
        self.qa_sentry = QASentry(self.watsonx)
        self.doc_engine = DocEngine(self.watsonx)
        self.file_manager = FileManager()
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all MCP tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools"""
            return [
                Tool(
                    name="scan_code_quality",
                    description="Analyze code for bugs, vulnerabilities, and quality issues using watsonx.ai",
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
                                "description": "Type of scan to perform"
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
                    name="read_dataset_file",
                    description="Read and analyze files from the dataset_balancia test project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Relative path within dataset_balancia/"
                            }
                        },
                        "required": ["file_path"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls"""
            
            if name == "scan_code_quality":
                result = await self.qa_sentry.scan_code(
                    arguments.get("file_path"),
                    arguments.get("scan_type", "all")
                )
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "generate_documentation":
                result = await self.doc_engine.generate_docs(
                    arguments.get("file_path"),
                    arguments.get("doc_type", "full")
                )
                return [TextContent(type="text", text=result)]
            
            elif name == "read_dataset_file":
                result = self.file_manager.read_dataset_file(
                    arguments.get("file_path")
                )
                return [TextContent(type="text", text=result)]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
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
