"""
Ideation Engine - Core Orchestrator
Transforms IBM Bob into a proactive Technical Product Manager

This is the main entry point. It orchestrates:
- Framework retrieval and display
- Input validation
- PRD synthesis via watsonx.ai
- Output formatting and file saving
"""

from typing import Dict, Any, Optional

from lib.ideation.framework import get_framework_definition
from lib.ideation.validators import validate_conversation_data, validate_project_name
from lib.ideation.formatters import (
    format_framework_for_display,
    format_prd_output,
    determine_output_path,
    save_prd_to_file,
    load_sample_prd,
    format_error_response,
    format_success_response
)
from lib.utils import get_timestamp


class IdeationEngine:
    """Production-grade feature planning with AI-driven conversation"""

    def __init__(self, watsonx_client):
        """
        Initialize Ideation Engine with AI capabilities.

        Args:
            watsonx_client: WatsonxClient instance for PRD synthesis
        """
        self.watsonx = watsonx_client

    # ------------------------------------------------------------------ #
    #                       FRAMEWORK RETRIEVAL                           #
    # ------------------------------------------------------------------ #

    def get_framework(self, include_examples: bool = True) -> Dict[str, Any]:
        """
        Retrieve the 7-pillar ideation framework.

        Args:
            include_examples: If True, include example answers for each pillar

        Returns:
            Dictionary containing the complete framework structure
        """
        framework = get_framework_definition()
        
        if not include_examples:
            # Remove examples from each pillar
            for pillar in framework["pillars"]:
                pillar.pop("examples", None)
        
        return framework

    def format_framework_for_display(self) -> str:
        """
        Format the framework as a readable markdown document for Bob to use.

        Returns:
            Markdown-formatted framework guide
        """
        return format_framework_for_display(include_examples=True)

    # ------------------------------------------------------------------ #
    #                       PRD SYNTHESIS                                 #
    # ------------------------------------------------------------------ #

    async def synthesize_prd(
        self,
        conversation_data: Dict[str, Any],
        project_name: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive PRD from conversation data.

        Args:
            conversation_data: Structured conversation data or transcript
            project_name: Name of the project/feature (optional)
            output_path: Custom path to save PRD (optional, AI can decide)

        Returns:
            Dictionary containing:
                - success: bool
                - prd_markdown: str (the generated PRD)
                - file_path: str (where it was saved, if applicable)
                - metadata: dict (generation info)
        """
        try:
            # Validate project name if provided
            if project_name and not validate_project_name(project_name):
                return format_error_response(
                    error="Invalid project name",
                    suggestions=["Use alphanumeric characters, hyphens, and underscores only"]
                )

            # Validate input
            validation_result = validate_conversation_data(conversation_data)
            if not validation_result["valid"]:
                return format_error_response(
                    error=validation_result["error"],
                    suggestions=validation_result.get("suggestions", [])
                )

            # Load sample PRD for reference
            sample_prd = load_sample_prd()

            # Generate PRD using watsonx.ai
            prd_markdown = await self.watsonx.synthesize_prd(
                conversation_data=conversation_data,
                sample_prd=sample_prd,
                project_name=project_name
            )

            # Determine output path (AI-driven or user-specified)
            final_output_path = determine_output_path(
                output_path=output_path,
                project_name=project_name
            )

            # Save to file
            file_saved = save_prd_to_file(prd_markdown, final_output_path)

            # Prepare metadata
            metadata = {
                "generated_at": get_timestamp(),
                "project_name": project_name or "Unnamed Project",
                "pillar_count": len(conversation_data.get("pillars", {})),
                "file_saved": file_saved,
                "output_path": final_output_path if file_saved else None
            }

            # Format final output
            formatted_prd = format_prd_output(
                prd_markdown=prd_markdown,
                metadata=metadata,
                file_path=final_output_path if file_saved else None
            )

            return format_success_response(
                prd_markdown=formatted_prd,
                file_path=final_output_path if file_saved else None,
                metadata=metadata
            )

        except Exception as e:
            return format_error_response(
                error=f"Error generating PRD: {str(e)}",
                error_type=type(e).__name__
            )


# Made with Bob