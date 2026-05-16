"""
Interactive Documentation Generator
Generate any of the 12 documentation types by simply running this script

Usage:
    python generate_docs.py wireframe path/to/file.ts
    python generate_docs.py user_manual path/to/file.py
    python generate_docs.py quick_start path/to/file.js
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.autodocs import AutoDocs
from watsonx_client import WatsonxClient


# Documentation type mappings for natural language prompts
DOC_TYPE_ALIASES = {
    # Direct types
    "user_manual": "user_manual",
    "how_to_guide": "how_to_guide",
    "quick_start": "quick_start",
    "tutorial": "tutorial",
    "troubleshooting": "troubleshooting",
    "user_persona": "user_persona",
    "knowledge_base": "knowledge_base",
    "ux_design": "ux_design",
    "wireframe": "wireframe",
    "requirements": "requirements",
    "api": "api",
    "full": "full",
    
    # Natural language aliases
    "manual": "user_manual",
    "guide": "how_to_guide",
    "quickstart": "quick_start",
    "quick-start": "quick_start",
    "tut": "tutorial",
    "troubleshoot": "troubleshooting",
    "persona": "user_persona",
    "kb": "knowledge_base",
    "ux": "ux_design",
    "design": "ux_design",
    "wire": "wireframe",
    "mockup": "wireframe",
    "req": "requirements",
    "spec": "requirements",
    "specification": "requirements",
    "api_doc": "api",
    "comprehensive": "full",
    "all": "full",
}


def print_help():
    """Print usage help"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    AUTODOCS - DOCUMENTATION GENERATOR                 ║
╚══════════════════════════════════════════════════════════════════════╝

USAGE:
    python generate_docs.py <doc_type> <file_path> [output_file]

EXAMPLES:
    python generate_docs.py wireframe src/app/page.tsx
    python generate_docs.py user_manual lib/utils.py my_manual.md
    python generate_docs.py quick_start index.js

DOCUMENTATION TYPES:
    1.  user_manual       - Comprehensive user manuals
    2.  how_to_guide      - Step-by-step how-to guides
    3.  quick_start       - Quick-start guides
    4.  tutorial          - Interactive tutorials
    5.  troubleshooting   - Troubleshooting guides
    6.  user_persona      - User personas
    7.  knowledge_base    - Internal knowledge base articles
    8.  ux_design         - UX design documentation
    9.  wireframe         - Wireframes and UI mockups
    10. requirements      - Software requirement specifications
    11. api               - API documentation
    12. full              - Comprehensive documentation (all types)

ALIASES (you can also use these):
    - manual, guide, quickstart, tut, troubleshoot, persona
    - kb, ux, design, wire, mockup, req, spec, api_doc, all

NATURAL LANGUAGE PROMPTS:
    You can also use natural language like:
    - "generate wireframe"
    - "create user manual"
    - "make quick start guide"
    
    The system will automatically detect the documentation type!
""")


def parse_natural_language_prompt(prompt: str) -> tuple[str | None, str | None]:
    """
    Parse natural language prompts to extract doc type and file path
    
    Examples:
        "generate wireframe for src/app.tsx" -> ("wireframe", "src/app.tsx")
        "create user manual" -> ("user_manual", None)
        "i want to generate the wireframe" -> ("wireframe", None)
    """
    prompt_lower = prompt.lower()
    
    # Check for each documentation type
    for alias, doc_type in DOC_TYPE_ALIASES.items():
        if alias in prompt_lower:
            # Try to extract file path
            parts = prompt.split()
            for i, part in enumerate(parts):
                if part.lower() == "for" and i + 1 < len(parts):
                    return doc_type, parts[i + 1]
                # Check if it's a file path
                if '/' in part or '\\' in part or '.' in part:
                    if not part.lower() in ['the', 'a', 'an']:
                        return doc_type, part
            
            return doc_type, None
    
    return None, None


async def generate_documentation(doc_type: str, file_path: str, output_file: str | None = None):
    """Generate documentation"""
    
    # Validate file exists
    if not Path(file_path).exists():
        print(f"[ERROR] File not found: {file_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"GENERATING DOCUMENTATION")
    print(f"{'='*70}")
    print(f"Type: {doc_type}")
    print(f"File: {file_path}")
    print(f"{'='*70}\n")
    
    # Initialize
    print("Initializing WatsonX client...")
    watsonx = WatsonxClient()
    autodocs = AutoDocs(watsonx)
    
    # Generate
    print(f"Generating {doc_type} documentation...")
    try:
        docs = await autodocs.generate_docs(file_path, doc_type)
        
        # Determine output file
        if not output_file:
            file_stem = Path(file_path).stem
            output_file = f"{file_stem}_{doc_type}.md"
        
        # Save
        Path(output_file).write_text(docs, encoding='utf-8')
        
        print(f"\n{'='*70}")
        print(f"[SUCCESS]")
        print(f"{'='*70}")
        print(f"Documentation saved to: {output_file}")
        print(f"{'='*70}\n")
        
        # Show preview
        lines = docs.split('\n')
        preview_lines = min(20, len(lines))
        print("PREVIEW:")
        print('-'*70)
        print('\n'.join(lines[:preview_lines]))
        if len(lines) > preview_lines:
            print(f"\n... ({len(lines) - preview_lines} more lines)")
        print('-'*70)
        
    except Exception as e:
        print(f"\n[ERROR] Error generating documentation: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Main function"""
    
    # Check if arguments provided
    if len(sys.argv) < 2:
        print_help()
        return
    
    # Parse arguments
    args = sys.argv[1:]
    
    # Check if it's a natural language prompt
    full_prompt = ' '.join(args)
    doc_type, file_path = parse_natural_language_prompt(full_prompt)
    
    if doc_type:
        print(f"\n[OK] Detected documentation type: {doc_type}")
        if not file_path:
            print("Please specify a file path:")
            file_path = input("File path: ").strip()
        
        output_file = None
        if len(args) > 2:
            output_file = args[2]
        
        await generate_documentation(doc_type, file_path, output_file)
    else:
        # Traditional argument parsing
        if len(args) < 2:
            print("[ERROR] Please specify documentation type and file path")
            print_help()
            return
        
        doc_type_input = args[0].lower()
        file_path = args[1]
        output_file = args[2] if len(args) > 2 else None
        
        # Map to actual doc type
        doc_type = DOC_TYPE_ALIASES.get(doc_type_input, doc_type_input)
        
        # Validate doc type
        valid_types = set(DOC_TYPE_ALIASES.values())
        if doc_type not in valid_types:
            print(f"[ERROR] Invalid documentation type: {doc_type_input}")
            print(f"\nValid types: {', '.join(sorted(valid_types))}")
            print_help()
            return
        
        await generate_documentation(doc_type, file_path, output_file)


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
