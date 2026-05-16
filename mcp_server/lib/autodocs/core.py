"""
Auto Docs - Core Documentation Generator
Generates comprehensive documentation for code using watsonx.ai
Supports 12 different documentation types for various use cases
"""

from typing import Dict, Any, Optional
from pathlib import Path
from lib.utils import detect_language, get_timestamp, read_file_safe, format_markdown_header
from .generators import (
    generate_api_reference,
    generate_usage_examples,
    generate_user_manual,
    generate_how_to_guide,
    generate_quick_start_guide,
    generate_tutorial,
    generate_troubleshooting_guide,
    generate_user_persona,
    generate_knowledge_base_article,
    generate_ux_design_doc,
    generate_wireframe,
    generate_software_requirements
)


class AutoDocs:
    """
    Automated documentation generation for code
    
    Supported Documentation Types:
    1. user_manual - Comprehensive user manuals
    2. how_to_guide - Step-by-step how-to guides
    3. quick_start - Quick-start guides
    4. tutorial - Interactive tutorials
    5. troubleshooting - Troubleshooting guides
    6. user_persona - User personas
    7. knowledge_base - Internal knowledge base articles
    8. ux_design - UX design documentation
    9. wireframe - Wireframes and UI mockups
    10. requirements - Software requirement specifications
    11. api - API documentation
    12. full - Comprehensive documentation (all types combined)
    """

    def __init__(self, watsonx_client):
        """
        Initialize Auto Docs

        Args:
            watsonx_client: WatsonxClient instance for AI-powered documentation
        """
        self.watsonx = watsonx_client
        
        # Map documentation types to their generator functions
        self.doc_generators = {
            "user_manual": generate_user_manual,
            "how_to_guide": generate_how_to_guide,
            "quick_start": generate_quick_start_guide,
            "tutorial": generate_tutorial,
            "troubleshooting": generate_troubleshooting_guide,
            "user_persona": generate_user_persona,
            "knowledge_base": generate_knowledge_base_article,
            "ux_design": generate_ux_design_doc,
            "wireframe": generate_wireframe,
            "requirements": generate_software_requirements,
            "api": generate_api_reference,
        }

    async def generate_docs(
        self,
        file_path: str,
        doc_type: str = "full"
    ) -> str:
        """
        Generate documentation for a code file.

        Args:
            file_path: Path to the code file
            doc_type: Type of documentation (user_manual, how_to_guide, quick_start,
                     tutorial, troubleshooting, user_persona, knowledge_base, ux_design,
                     wireframe, requirements, api, full)

        Returns:
            Generated documentation as string
        """
        # Read the file
        code, error = read_file_safe(file_path)
        if error:
            return f"Error: {error}"
        
        # Type guard: ensure code is not None before proceeding
        if code is None:
            return f"Error: Failed to read file {file_path}"

        # Detect language
        language = detect_language(file_path)
        lang = language or "unknown"

        # Generate documentation based on type
        if doc_type == "full":
            # Generate comprehensive documentation with all types
            documentation = await self._generate_full_documentation(code, file_path, lang)
        elif doc_type in self.doc_generators:
            # Generate specific documentation type
            prompt = self._build_documentation_prompt(code, doc_type, language)
            ai_content = await self.watsonx.generate_text(prompt, temperature=0.5)
            
            # Use the specialized generator to format the output
            generator_func = self.doc_generators[doc_type]
            documentation = generator_func(code, lang, ai_content)
        else:
            # Fallback to basic documentation
            prompt = self._build_documentation_prompt(code, "api", language)
            documentation = await self.watsonx.generate_text(prompt, temperature=0.5)

        # Format the documentation with metadata
        formatted_docs = self._format_documentation(
            documentation,
            file_path,
            doc_type,
            lang
        )

        return formatted_docs

    async def _generate_full_documentation(
        self,
        code: str,
        file_path: str,
        language: str
    ) -> str:
        """Generate comprehensive documentation with all types"""
        sections = []
        
        # Generate each documentation type
        doc_types = [
            ("API Documentation", "api"),
            ("Quick Start Guide", "quick_start"),
            ("User Manual", "user_manual"),
            ("How-To Guide", "how_to_guide"),
            ("Tutorial", "tutorial"),
            ("Troubleshooting Guide", "troubleshooting"),
            ("Requirements Specification", "requirements"),
        ]
        
        for section_name, doc_type in doc_types:
            prompt = self._build_documentation_prompt(code, doc_type, language)
            content = await self.watsonx.generate_text(prompt, temperature=0.5)
            
            sections.append(f"\n## {section_name}\n\n{content}")
        
        return "\n".join(sections)

    def _build_documentation_prompt(
        self,
        code: str,
        doc_type: str,
        language: Optional[str]
    ) -> str:
        """Build prompt for documentation generation based on type"""
        lang_hint = f" ({language})" if language else ""

        prompts = {
            "user_manual": f"""Generate a comprehensive user manual for the following code{lang_hint}.
Include:
- Overview and purpose
- Installation instructions
- Configuration options
- Usage examples
- Common use cases
- Best practices

Code:
{code}""",

            "how_to_guide": f"""Generate a step-by-step how-to guide for the following code{lang_hint}.
Include:
- Clear objective
- Prerequisites
- Step-by-step instructions
- Expected outcomes
- Tips and warnings

Code:
{code}""",

            "quick_start": f"""Generate a quick-start guide for the following code{lang_hint}.
Include:
- Minimal setup steps
- Basic usage example
- Next steps
- Links to detailed documentation

Code:
{code}""",

            "tutorial": f"""Generate an interactive tutorial for the following code{lang_hint}.
Include:
- Learning objectives
- Prerequisites
- Step-by-step lessons
- Practice exercises
- Summary and next steps

Code:
{code}""",

            "troubleshooting": f"""Generate a troubleshooting guide for the following code{lang_hint}.
Include:
- Common errors and solutions
- Debugging steps
- FAQ
- Known issues
- Support resources

Code:
{code}""",

            "user_persona": f"""Generate user personas for the following code{lang_hint}.
Include:
- User types and roles
- Goals and motivations
- Pain points
- Technical skill level
- Use case scenarios

Code:
{code}""",

            "knowledge_base": f"""Generate a knowledge base article for the following code{lang_hint}.
Include:
- Article title and summary
- Problem description
- Solution steps
- Related articles
- Tags and categories

Code:
{code}""",

            "ux_design": f"""Generate UX design documentation for the following code{lang_hint}.
Include:
- User interface components
- User flows
- Interaction patterns
- Accessibility considerations
- Design principles

Code:
{code}""",

            "wireframe": f"""Generate wireframe documentation for the following code{lang_hint}.
Include:
- Screen layouts (ASCII art or description)
- Component hierarchy
- Navigation flow
- Interactive elements
- Responsive design notes

Code:
{code}""",

            "requirements": f"""Generate software requirements specification for the following code{lang_hint}.
Include:
- Functional requirements
- Non-functional requirements
- System constraints
- Dependencies
- Acceptance criteria

Code:
{code}""",

            "api": f"""Generate API documentation for the following code{lang_hint}.
Include:
- Endpoints/Functions
- Parameters and types
- Return values
- Error codes
- Usage examples

Code:
{code}""",
        }

        return prompts.get(doc_type, prompts["api"])

    def _format_documentation(
        self,
        documentation: str,
        file_path: str,
        doc_type: str,
        language: str
    ) -> str:
        """Format the generated documentation with metadata"""
        doc_type_names = {
            "user_manual": "User Manual",
            "how_to_guide": "How-To Guide",
            "quick_start": "Quick Start Guide",
            "tutorial": "Tutorial",
            "troubleshooting": "Troubleshooting Guide",
            "user_persona": "User Persona",
            "knowledge_base": "Knowledge Base Article",
            "ux_design": "UX Design Documentation",
            "wireframe": "Wireframe Documentation",
            "requirements": "Software Requirements Specification",
            "api": "API Documentation",
            "full": "Comprehensive Documentation"
        }
        
        doc_name = doc_type_names.get(doc_type, doc_type.title())
        
        header = format_markdown_header(f"{doc_name} for {Path(file_path).name}", {
            "file": file_path,
            "language": language,
            "documentation_type": doc_name,
            "generated": get_timestamp()
        })

        return header + "\n" + documentation

# Made with Bob
