"""
Visualizer Engine Prompts - Centralized prompt templates for diagram generation
Extracted for better maintainability and versioning
"""

from typing import Dict, Any


def build_feature_flow_prompt(project_name: str, structure: str, key_files: str) -> str:
    """
    Build prompt for feature flow analysis.
    
    Args:
        project_name: Name of the project
        structure: File structure context
        key_files: Key file contents
    
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are an elite software architect. Analyze this system configuration and output valid JSON mapping core operational routes.
Project name: {project_name}
Files layout context:
{structure}

Key File Sample Configurations:
{key_files}

Task: Identify main systemic workflows. Return strict valid JSON with NO markdown formatting outside the JSON block object itself:
{{
  "features": [
    {{
      "name": "Feature Title",
      "description": "Functional description",
      "entry_point": "file_path.py",
      "flow_steps": [
        {{"actor": "User", "action": "Interacts with UI", "target": "Controller"}}
      ]
    }}
  ]
}}"""
    
    return prompt


def build_project_concept_prompt(project_name: str, structure: str) -> str:
    """
    Build prompt for project concept analysis.
    
    Args:
        project_name: Name of the project
        structure: File structure context
    
    Returns:
        Formatted prompt string
    """
    prompt = f"""Analyze systemic dependencies and build an structural architectural outline model.
Project Root: {project_name}
File System:
{structure}

Return strict structural architecture maps as JSON format matching blueprint details:
{{
  "project_type": "Web App / Microservice / CLI",
  "description": "High level summary description",
  "components": [
    {{
      "name": "Component Module",
      "type": "ui/server/database/api/external",
      "description": "Responsibilities",
      "connects_to": []
    }}
  ],
  "external_services": []
}}"""
    
    return prompt


# Made with Bob