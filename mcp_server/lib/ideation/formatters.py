"""
Ideation Engine - Output Formatters
Formats framework and PRD output for display
"""

from typing import Dict, Any
from datetime import datetime
from pathlib import Path
from lib.utils import format_markdown_header, get_timestamp
from lib.ideation.framework import get_framework_definition


def format_framework_for_display(include_examples: bool = True) -> str:
    """
    Format the framework as a readable markdown document for Bob to use.
    
    Args:
        include_examples: Whether to include example answers
        
    Returns:
        Markdown-formatted framework guide
    """
    framework = get_framework_definition()
    
    lines = [
        format_markdown_header("🧠 Ideation Framework - 7 Pillars", {
            "version": framework["meta"]["version"],
            "purpose": framework["meta"]["purpose"]
        })
    ]

    for i, pillar in enumerate(framework["pillars"], 1):
        lines.append(f"\n## Pillar {i}: {pillar['title']}")
        lines.append(f"\n**Importance:** {pillar['importance']}")
        lines.append(f"\n\n{pillar['prompt']}")
        lines.append(f"\n\n💡 **Guidance:** {pillar['guidance']}")
        
        if include_examples and pillar.get("examples"):
            lines.append("\n\n**Examples:**")
            for example in pillar["examples"]:
                lines.append(f"\n- {example}")
        
        lines.append("\n\n---")

    lines.append("\n\n## 🎯 How to Use This Framework")
    lines.append("\n\n1. Bob will guide you through each pillar sequentially")
    lines.append("\n2. Answer thoughtfully - quality input = quality PRD")
    lines.append("\n3. Bob may ask follow-up questions for clarity")
    lines.append("\n4. After all pillars are complete, Bob will synthesize your PRD")
    lines.append("\n5. The PRD will be returned in chat and saved to a file")

    return "".join(lines)


def format_prd_output(
    prd_markdown: str,
    metadata: Dict[str, Any],
    file_path: str = None
) -> str:
    """
    Format the final PRD output with metadata footer.
    
    Args:
        prd_markdown: The generated PRD content
        metadata: Generation metadata
        file_path: Path where PRD was saved (optional)
        
    Returns:
        Formatted PRD with metadata footer
    """
    lines = [prd_markdown]
    
    # Add separator
    lines.append("\n\n---\n")
    
    # Add metadata
    lines.append(f"\n**Generated:** {metadata.get('generated_at', get_timestamp())}")
    lines.append(f"\n**Project:** {metadata.get('project_name', 'Unnamed Project')}")
    lines.append(f"\n**Pillars Completed:** {metadata.get('pillar_count', 'N/A')}")
    
    if file_path:
        lines.append(f"\n**Saved to:** `{file_path}`")
    
    lines.append("\n\n*Made with IBM Bob* 🤖")
    
    return "".join(lines)


def determine_output_path(
    output_path: str = None,
    project_name: str = None
) -> str:
    """
    Determine where to save the PRD file.
    
    Args:
        output_path: User-specified path (takes precedence)
        project_name: Project name for filename generation
        
    Returns:
        Path string for saving the PRD
    """
    # If user specified a path, use it
    if output_path:
        return output_path

    # Otherwise, generate a smart path based on project name
    from lib.ideation.validators import sanitize_project_name
    safe_name = sanitize_project_name(project_name)

    # Generate timestamp-based filename
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"{safe_name}-prd-{timestamp}.md"

    # Default to ideation directory
    ideation_dir = Path(__file__).parent
    return str(ideation_dir / filename)


def save_prd_to_file(prd_content: str, output_path: str) -> bool:
    """
    Save PRD to file with error handling.
    
    Args:
        prd_content: The markdown content to save
        output_path: Path where to save the file
        
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        output_file = Path(output_path)
        
        # Create parent directories if they don't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prd_content)
        
        return True
    except Exception as e:
        # Log error but don't fail the entire operation
        print(f"Warning: Failed to save PRD to {output_path}: {str(e)}")
        return False


def load_sample_prd() -> str:
    """
    Load the sample PRD for reference.
    
    Returns:
        Sample PRD content or empty string if not found
    """
    try:
        sample_path = Path(__file__).parent / "sample-prd.md"
        with open(sample_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        # Return empty string if sample not found
        return ""


def format_error_response(
    error: str,
    suggestions: list = None,
    error_type: str = None
) -> Dict[str, Any]:
    """
    Format an error response with helpful information.
    
    Args:
        error: Error message
        suggestions: List of suggestions to fix the error
        error_type: Type of error (optional)
        
    Returns:
        Formatted error response dictionary
    """
    response = {
        "success": False,
        "error": error
    }
    
    if suggestions:
        response["suggestions"] = suggestions
    
    if error_type:
        response["error_type"] = error_type
    
    return response


def format_success_response(
    prd_markdown: str,
    file_path: str = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format a success response with PRD and metadata.
    
    Args:
        prd_markdown: The generated PRD content
        file_path: Path where PRD was saved (optional)
        metadata: Generation metadata (optional)
        
    Returns:
        Formatted success response dictionary
    """
    if metadata is None:
        metadata = {
            "generated_at": get_timestamp(),
            "project_name": "Unnamed Project",
            "pillar_count": 0,
            "file_saved": file_path is not None
        }
    
    return {
        "success": True,
        "prd_markdown": prd_markdown,
        "file_path": file_path,
        "metadata": metadata
    }


# Made with Bob