"""
Ideation Engine Prompts - Centralized prompt templates for PRD generation
Extracted from watsonx_client.py for better maintainability
"""

from typing import Dict, Any, Optional


def build_prd_synthesis_prompt(
    conversation_data: Dict[str, Any],
    sample_prd: str,
    project_name: Optional[str]
) -> str:
    """
    Build a comprehensive prompt for PRD synthesis.
    
    This prompt instructs the AI to act as a Senior Technical Product Manager
    and synthesize the conversation into a professional PRD.
    
    Args:
        conversation_data: Structured conversation or transcript data
        sample_prd: Sample PRD for reference formatting
        project_name: Name of the project/feature
    
    Returns:
        Formatted prompt string
    """
    # Extract conversation type
    conversation_type = conversation_data.get("conversation_type", "structured")
    
    # Format the conversation data
    if conversation_type == "structured":
        conversation_text = _format_structured_conversation(conversation_data)
    else:
        conversation_text = _format_transcript_conversation(conversation_data)
    
    # Build the prompt
    project_title = project_name or "New Feature"
    
    prompt = f"""You are a Senior Technical Product Manager at a leading tech company. Your task is to synthesize a comprehensive Product Requirements Document (PRD) from a feature planning conversation.

# YOUR ROLE
- Transform raw conversation data into a polished, professional PRD
- Maintain technical accuracy while ensuring clarity
- Structure information logically and actionably
- Add insights and recommendations where appropriate
- Ensure the PRD is ready for engineering teams to implement

# CONVERSATION DATA
The following is a structured conversation covering 7 key planning pillars:

{conversation_text}

# SAMPLE PRD STRUCTURE (for reference)
{sample_prd if sample_prd else "Use standard PRD format with Overview, Features, Technical Requirements, Success Criteria, Timeline, and Resources sections."}

# YOUR TASK
Generate a comprehensive PRD for "{project_title}" that includes:

1. **Overview Section**
   - Clear project description
   - Target audience and value proposition
   - Problem statement and solution approach

2. **Scope Definition**
   - In Scope: Features included in MVP (be specific)
   - Out of Scope: Explicitly excluded features

3. **Technical Requirements**
   - Proposed architecture and technology stack
   - API design considerations
   - Database schema hints
   - Infrastructure needs

4. **Success Criteria**
   - Measurable acceptance criteria
   - Performance benchmarks
   - Quality gates

5. **Timeline & Milestones**
   - Project phases with timeframes
   - Key milestones and deliverables
   - Risk buffers

6. **Resources & Team**
   - Required team composition
   - Tools and infrastructure
   - Budget considerations
   - Dependencies

7. **Additional Sections** (if relevant)
   - User stories or use cases
   - Security considerations
   - Scalability plans
   - Future enhancements

# OUTPUT REQUIREMENTS
- Use clear, professional markdown formatting
- Include headers, bullet points, and code blocks where appropriate
- Be specific and actionable - avoid vague statements
- Maintain a balance between detail and readability
- Add a "Made with IBM Bob" footer

Generate the PRD now:"""
    
    return prompt


def _format_structured_conversation(conversation_data: Dict[str, Any]) -> str:
    """Format structured conversation data into readable text."""
    pillars = conversation_data.get("pillars", {})
    formatted_parts = []
    
    for pillar_name, pillar_data in pillars.items():
        formatted_parts.append(f"## {pillar_name}")
        if isinstance(pillar_data, dict):
            # Handle nested dictionary structure
            for key, value in pillar_data.items():
                formatted_parts.append(f"**{key}:** {value}")
        elif isinstance(pillar_data, str):
            # Handle simple string values
            formatted_parts.append(pillar_data)
        else:
            # Handle any other type
            formatted_parts.append(str(pillar_data))
        formatted_parts.append("")
    
    return "\n".join(formatted_parts)


def _format_transcript_conversation(conversation_data: Dict[str, Any]) -> str:
    """Format transcript-style conversation data into readable text."""
    transcript = conversation_data.get("transcript", "")
    return f"## Conversation Transcript\n\n{transcript}"


# Made with Bob