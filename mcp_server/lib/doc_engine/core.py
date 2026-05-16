"""
Doc Engine - Core Documentation Generator
Generates comprehensive documentation for code using watsonx.ai
"""

from typing import Dict, Any, Optional
from pathlib import Path
from lib.utils import detect_language, get_timestamp, read_file_safe, format_markdown_header


class DocEngine:
    """Automated documentation generation for code"""

    def __init__(self, watsonx_client):
        """
        Initialize Doc Engine

        Args:
            watsonx_client: WatsonxClient instance for AI-powered documentation
        """
        self.watsonx = watsonx_client

    async def generate_docs(
        self,
        file_path: str,
        doc_type: str = "full"
    ) -> str:
        """
        Generate documentation for a code file.

        Args:
            file_path: Path to the code file
            doc_type: Type of documentation (inline, api, readme, full)

        Returns:
            Generated documentation as string
        """
        # Read the file
        code, error = read_file_safe(file_path)
        if error:
            return f"Error: {error}"

        # Detect language
        language = detect_language(file_path)

        # Generate documentation
        prompt = self._build_documentation_prompt(code, doc_type, language)
        documentation = await self.watsonx.generate_text(prompt, temperature=0.5)

        # Format the documentation
        formatted_docs = self._format_documentation(
            documentation,
            file_path,
            doc_type,
            language
        )

        return formatted_docs

    def _build_documentation_prompt(
        self,
        code: str,
        doc_type: str,
        language: Optional[str]
    ) -> str:
        """Build prompt for documentation generation"""
        lang_hint = f" ({language})" if language else ""

        prompts = {
            "inline": f"Add inline comments and docstrings to the following code{lang_hint}:\n\n{code}",
            "api": f"Generate API documentation for the following code{lang_hint}:\n\n{code}",
            "readme": f"Generate a README.md section documenting the following code{lang_hint}:\n\n{code}",
            "full": f"Generate comprehensive documentation including inline comments, API docs, and usage examples for the following code{lang_hint}:\n\n{code}"
        }

        return prompts.get(doc_type, prompts["full"])

    def _format_documentation(
        self,
        documentation: str,
        file_path: str,
        doc_type: str,
        language: str
    ) -> str:
        """Format the generated documentation with metadata"""
        header = format_markdown_header(f"Documentation for {Path(file_path).name}", {
            "file": file_path,
            "language": language,
            "documentation_type": doc_type,
            "generated": get_timestamp()
        })

        return header + "\n" + documentation
