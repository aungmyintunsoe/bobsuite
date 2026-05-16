"""
Auto Docs - Automated Documentation Generation
Generates comprehensive documentation for code using watsonx.ai
"""

from .core import AutoDocs
from .generators import (
    generate_project_docs,
    generate_api_reference,
    generate_usage_examples,
    generate_readme
)

__all__ = [
    'AutoDocs',
    'generate_project_docs',
    'generate_api_reference',
    'generate_usage_examples',
    'generate_readme'
]

# Made with Bob
