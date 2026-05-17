"""
AutoDocs Prompts - Centralized prompt templates for documentation generation
Extracted for easier maintenance, versioning, and A/B testing
"""

from typing import Optional

def get_documentation_prompt(code: str, doc_type: str, language: Optional[str] = None) -> str:
    """
    Get the appropriate prompt for a documentation type.
    
    Args:
        code: Source code to document
        doc_type: Type of documentation to generate
        language: Programming language (optional)
    
    Returns:
        Formatted prompt string
    """
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


# Made with Bob