"""
Ideation Engine - Input Validators
Validates conversation data before PRD synthesis
"""

from typing import Dict, Any, List, Optional
from lib.ideation.framework import get_critical_pillars, get_pillar_by_id


def validate_conversation_data(conversation_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate conversation data before synthesis.
    
    Args:
        conversation_data: The conversation data to validate
        
    Returns:
        Dictionary with validation results:
            - valid: bool
            - error: str (if invalid)
            - suggestions: list (if invalid)
    """
    if not conversation_data:
        return {
            "valid": False,
            "error": "Conversation data is empty",
            "suggestions": ["Start the ideation process by answering the framework questions"]
        }

    # Check conversation type
    conversation_type = conversation_data.get("conversation_type", "structured")
    
    if conversation_type == "structured":
        return _validate_structured_data(conversation_data)
    elif conversation_type == "transcript":
        return _validate_transcript_data(conversation_data)
    else:
        return {
            "valid": False,
            "error": f"Unknown conversation type: {conversation_type}",
            "suggestions": ["Use 'structured' or 'transcript' as conversation_type"]
        }


def _validate_structured_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate structured pillar-based conversation data"""
    pillars = data.get("pillars", {})
    
    if not pillars:
        return {
            "valid": False,
            "error": "No pillar responses found",
            "suggestions": ["Answer at least the critical pillars: description, in_scope, acceptance, timeline"]
        }

    # Check critical pillars
    critical_pillars = get_critical_pillars()
    missing_critical = []
    
    for pillar_id in critical_pillars:
        if pillar_id not in pillars:
            missing_critical.append(pillar_id)
        else:
            pillar_value = pillars[pillar_id]
            # Handle both dict format {"answer": "text"} and simple string format
            if isinstance(pillar_value, dict):
                if not pillar_value.get("answer"):
                    missing_critical.append(pillar_id)
            elif isinstance(pillar_value, str):
                if not pillar_value.strip():
                    missing_critical.append(pillar_id)
            else:
                missing_critical.append(pillar_id)
    
    if missing_critical:
        pillar_names = []
        for pid in missing_critical:
            pillar_def = get_pillar_by_id(pid)
            if pillar_def:
                pillar_names.append(pillar_def["title"])
        return {
            "valid": False,
            "error": f"Missing critical pillars: {', '.join(missing_critical)}",
            "suggestions": [f"Please provide answers for: {', '.join(pillar_names)}"] if pillar_names else ["Check pillar IDs against framework definition"]
        }

    # Check minimum response lengths
    for pillar_id, pillar_data in pillars.items():
        # Handle both dict format {"answer": "text"} and simple string format
        if isinstance(pillar_data, dict):
            answer = pillar_data.get("answer", "")
        elif isinstance(pillar_data, str):
            answer = pillar_data
        else:
            answer = str(pillar_data)
            
        pillar_def = get_pillar_by_id(pillar_id)
        
        if not pillar_def:
            continue
            
        min_length = pillar_def.get("min_length", 20)
        
        if len(answer.strip()) < min_length:
            return {
                "valid": False,
                "error": f"Response for '{pillar_id}' is too short (minimum {min_length} characters, got {len(answer.strip())})",
                "suggestions": [
                    f"Provide more detailed answer for '{pillar_def['title']}'",
                    "Quality PRDs require comprehensive responses"
                ]
            }

    return {"valid": True}


def _validate_transcript_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate raw transcript conversation data"""
    messages = data.get("messages", [])
    
    if len(messages) < 10:  # At least 5 Q&A pairs
        return {
            "valid": False,
            "error": "Conversation transcript is too short",
            "suggestions": [
                "Complete the full ideation interview before generating PRD",
                "Minimum 10 messages (5 question-answer pairs) required"
            ]
        }
    
    # Check for alternating roles
    has_assistant = any(msg.get("role") == "assistant" for msg in messages)
    has_user = any(msg.get("role") == "user" for msg in messages)
    
    if not (has_assistant and has_user):
        return {
            "valid": False,
            "error": "Transcript must contain both assistant and user messages",
            "suggestions": ["Ensure the conversation includes both Bob's questions and your answers"]
        }
    
    # Check message content length
    total_content_length = sum(len(msg.get("content", "")) for msg in messages)
    if total_content_length < 500:
        return {
            "valid": False,
            "error": "Conversation content is too brief for quality PRD generation",
            "suggestions": ["Provide more detailed responses to Bob's questions"]
        }

    return {"valid": True}


def validate_project_name(project_name: Optional[str]) -> bool:
    """
    Validate project name for file naming.
    
    Args:
        project_name: The project name to validate
        
    Returns:
        True if valid or None, False if invalid
    """
    if project_name is None:
        return True
    
    if not project_name.strip():
        return False
    
    if len(project_name) > 100:
        return False
    
    # Check for invalid filename characters
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    if any(char in project_name for char in invalid_chars):
        return False
    
    return True


def sanitize_project_name(project_name: Optional[str]) -> str:
    """
    Sanitize project name for use in filenames.
    
    Args:
        project_name: The project name to sanitize
        
    Returns:
        Sanitized project name safe for filenames
    """
    if not project_name:
        return "project"
    
    # Replace invalid characters with hyphens
    safe_name = "".join(
        c if c.isalnum() or c in ('-', '_', ' ') else '-' 
        for c in project_name
    )
    
    # Replace spaces with hyphens
    safe_name = safe_name.replace(' ', '-')
    
    # Remove consecutive hyphens
    while '--' in safe_name:
        safe_name = safe_name.replace('--', '-')
    
    # Trim and lowercase
    safe_name = safe_name.strip('-').lower()
    
    # Limit length
    safe_name = safe_name[:50]
    
    return safe_name or "project"


# Made with Bob