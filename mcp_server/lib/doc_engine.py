"""
Doc Engine - Documentation Generation Module
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
        Generate documentation for a code file
        
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
    
    async def generate_project_docs(
        self,
        project_path: str,
        output_dir: str = "docs",
        file_patterns: Optional[list] = None
    ) -> Dict[str, Any]:
        """Generate documentation for an entire project"""
        if file_patterns is None:
            file_patterns = ['*.py', '*.js', '*.ts', '*.java']
        
        project_root = Path(project_path)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {
            "success": True,
            "files_processed": 0,
            "files_failed": 0,
            "output_directory": str(output_path),
            "files": []
        }
        
        # Find all matching files
        files_to_document = []
        for pattern in file_patterns:
            files_to_document.extend(project_root.rglob(pattern))
        
        # Generate docs for each file
        for file_path in files_to_document:
            try:
                docs = await self.generate_docs(str(file_path), "full")
                
                # Save to output directory
                relative_path = file_path.relative_to(project_root)
                output_file = output_path / f"{relative_path}.md"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(docs)
                
                results["files_processed"] += 1
                results["files"].append({
                    "source": str(file_path),
                    "output": str(output_file),
                    "status": "success"
                })
                
            except Exception as e:
                results["files_failed"] += 1
                results["files"].append({
                    "source": str(file_path),
                    "status": "failed",
                    "error": str(e)
                })
        
        return results
    
    def generate_api_reference(
        self,
        code: str,
        language: str
    ) -> str:
        """Generate API reference documentation"""
        api_ref = [
            "# API Reference\n",
            f"**Language:** {language}\n",
            "\n## Overview\n",
            "\nThis section provides API documentation for the code.\n",
            "\n## Functions and Methods\n",
            "\n(Generated by watsonx.ai)\n"
        ]
        
        return "".join(api_ref)
    
    def generate_usage_examples(
        self,
        code: str,
        language: str
    ) -> str:
        """Generate usage examples for code"""
        examples = [
            "# Usage Examples\n",
            f"\n**Language:** {language}\n",
            "\n## Basic Usage\n",
            "\n```" + language.lower() + "\n",
            "// Example usage will be generated here\n",
            "```\n"
        ]
        
        return "".join(examples)
    
    async def generate_readme(
        self,
        project_path: str,
        project_name: Optional[str] = None
    ) -> str:
        """Generate a README.md for a project"""
        if project_name is None:
            project_name = Path(project_path).name
        
        # Analyze project structure
        project_root = Path(project_path)
        files = list(project_root.rglob("*"))
        
        readme = [
            f"# {project_name}\n",
            f"\n**Generated:** {get_timestamp()}\n",
            "\n## Overview\n",
            "\nThis project contains the following structure:\n",
            "\n## Project Structure\n",
            "\n```",
            f"\n{project_name}/",
        ]
        
        # Add file tree (simplified)
        for file in sorted(files)[:20]:  # Limit to first 20 files
            if file.is_file():
                relative = file.relative_to(project_root)
                readme.append(f"\n├── {relative}")
        
        readme.append("\n```\n")
        readme.append("\n## Installation\n")
        readme.append("\n(Installation instructions will be added here)\n")
        readme.append("\n## Usage\n")
        readme.append("\n(Usage instructions will be added here)\n")
        readme.append("\n## License\n")
        readme.append("\n(License information will be added here)\n")
        
        return "".join(readme)

# Made with Bob
