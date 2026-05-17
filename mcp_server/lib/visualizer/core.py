"""
Visualizer Engine - Core Orchestrator
Auto-generates visual diagrams for project onboarding

OPTIMIZATIONS:
- Extracted prompts for easier maintenance
- Ready for modular refactoring (dependency_analyzer, feature_mapper, etc.)
"""

import ast
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from collections import defaultdict

# Preserving your framework utility imports
from lib.utils import detect_language, read_file_safe, get_timestamp
from lib.visualizer.prompts import build_feature_flow_prompt, build_project_concept_prompt


class VisualizerEngine:
    """Production-grade visualization generator for project onboarding"""

    def __init__(self, watsonx_client):
        self.watsonx = watsonx_client

    def _get_file_content(self, filepath: str) -> str:
        """Safely extracts text content, handling if read_file_safe returns a Tuple"""
        result = read_file_safe(filepath)
        # If your util returns (content, error_msg), grab just the content
        if isinstance(result, tuple):
            return result[0] if result[0] else ""
        return result if result else ""

    # ------------------------------------------------------------------ #
    #                     DEPENDENCY CHAIN ANALYZER                      #
    # ------------------------------------------------------------------ #

    async def generate_dependency_chain(
        self,
        project_path: str,
        output_path: Optional[str] = None,
        max_depth: int = 3,
        include_external: bool = False
    ) -> Dict[str, Any]:
        """Generate a dependency chain diagram showing grouped module relationships."""
        try:
            target_path = Path(project_path).resolve()
            if not target_path.exists():
                return {"success": False, "error": f"Project path does not exist: {target_path}"}

            local_roots = {p.name for p in target_path.iterdir() if p.is_dir() and not p.name.startswith(('.', '__'))}
            local_roots.add(target_path.name)

            dependencies = self._analyze_dependencies(target_path, max_depth, include_external, local_roots)
            mermaid_diagram = self._create_dependency_mermaid(dependencies)
            markdown = self._format_dependency_output(mermaid_diagram, dependencies, target_path)

            save_path = self._save_visualization(markdown, output_path, "dependency-chain") if output_path else None

            return {
                "success": True,
                "diagram_type": "dependency_chain",
                "markdown": markdown,
                "mermaid": mermaid_diagram,
                "saved_to": save_path,
                "stats": {
                    "total_modules": len(dependencies["modules"]),
                    "total_dependencies": len(dependencies["edges"]),
                    "external_deps": len(dependencies["external"])
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to generate dependency chain: {str(e)}"}

    def _analyze_dependencies(self, target_path: Path, max_depth: int, include_external: bool, local_roots: Set[str]) -> Dict[str, Any]:
        modules = {}
        edges = []
        external = set()
        
        python_files = [f for f in target_path.rglob("*.py") if not any(k in f.parts for k in ("__pycache__", "venv", ".venv", "env"))]
        
        for file_path in python_files:
            module_name = self._get_module_name(file_path, target_path)
            if len(module_name.split('.')) > max_depth:
                continue
                
            modules[module_name] = str(file_path.relative_to(target_path))
            imports = self._parse_imports(file_path, local_roots)
            
            for imp in imports:
                if imp["is_external"]:
                    if include_external:
                        external.add(imp["module"])
                        edges.append((module_name, imp["module"], imp["type"]))
                else:
                    edges.append((module_name, imp["module"], imp["type"]))
        
        return {"modules": modules, "edges": edges, "external": list(external)}

    def _parse_imports(self, file_path: Path, local_roots: Set[str]) -> List[Dict[str, Any]]:
        imports = []
        content = self._get_file_content(str(file_path))
        if not content:
            return imports

        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base_mod = alias.name.split('.')[0]
                        imports.append({"module": base_mod, "full_name": alias.name, "type": "import", "is_external": base_mod not in local_roots})
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        base_mod = node.module.split('.')[0]
                        imports.append({"module": base_mod, "full_name": node.module, "type": "from", "is_external": base_mod not in local_roots and not node.level > 0})
        except Exception:
            imports = self._parse_imports_regex(content, local_roots)
        return imports

    def _parse_imports_regex(self, content: str, local_roots: Set[str]) -> List[Dict[str, Any]]:
        imports = []
        pattern = r'^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))'
        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                module = match.group(1) or match.group(2)
                base_mod = module.split('.')[0]
                imports.append({"module": base_mod, "full_name": module, "type": "from" if match.group(1) else "import", "is_external": base_mod not in local_roots})
        return imports

    def _get_module_name(self, file_path: Path, project_root: Path) -> str:
        rel_path = file_path.relative_to(project_root)
        module_parts = list(rel_path.parts[:-1]) + [rel_path.stem]
        if module_parts and module_parts[-1] == "__init__":
            module_parts = module_parts[:-1]
        return ".".join(module_parts) if module_parts else "root"

    def _create_dependency_mermaid(self, dependencies: Dict[str, Any]) -> str:
        lines = ["```mermaid", "graph TD"]
        subgraphs = defaultdict(list)
        
        for module_name in dependencies["modules"].keys():
            root_part = module_name.split('.')[0] if '.' in module_name else "Root"
            subgraphs[root_part].append(module_name)
            
        for group, elements in subgraphs.items():
            lines.append(f"    subgraph {group} [{group.upper()} Layer]")
            for mod in elements:
                safe_id = mod.replace(".", "_")
                display_name = mod.split(".")[-1]
                lines.append(f"        {safe_id}[{display_name}]")
            lines.append("    end")

        if dependencies["external"]:
            lines.append("    subgraph External [External Packages]")
            for ext in dependencies["external"]:
                safe_id = f"ext_{ext.replace('.', '_')}"
                lines.append(f"        {safe_id}[({ext})]")
            lines.append("    end")

        added_edges = set()
        for from_mod, to_mod, imp_type in dependencies["edges"]:
            from_id = from_mod.replace(".", "_")
            if to_mod in dependencies["external"]:
                to_id = f"ext_{to_mod.replace('.', '_')}"
                style = "-.->|depends on|"
            else:
                to_id = to_mod.replace(".", "_")
                style = "-->"
                
            edge_key = (from_id, to_id)
            if edge_key not in added_edges and from_id != to_id:
                lines.append(f"    {from_id} {style} {to_id}")
                added_edges.add(edge_key)

        lines.append("```")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #                         FEATURE FLOW MAPPER                        #
    # ------------------------------------------------------------------ #

    async def generate_feature_flow(self, project_path: str, feature_name: Optional[str] = None, output_path: Optional[str] = None) -> Dict[str, Any]:
        try:
            target_path = Path(project_path).resolve()
            analysis = await self._analyze_features_with_ai(target_path, feature_name)
            mermaid_diagram = self._create_feature_flow_mermaid(analysis)
            markdown = self._format_feature_flow_output(mermaid_diagram, analysis, target_path)
            save_path = self._save_visualization(markdown, output_path, "feature-flow") if output_path else None
            
            return {"success": True, "diagram_type": "feature_flow", "markdown": markdown, "mermaid": mermaid_diagram, "saved_to": save_path, "features_analyzed": len(analysis.get("features", []))}
        except Exception as e:
            return {"success": False, "error": f"Failed to generate feature flow: {str(e)}"}

    async def _analyze_features_with_ai(self, target_path: Path, feature_name: Optional[str]) -> Dict[str, Any]:
        context = self._gather_project_context(target_path)
        prompt = build_feature_flow_prompt(
            project_name=target_path.name,
            structure=context["structure"],
            key_files=context["key_files"]
        )
        response = await self.watsonx.generate_text(prompt=prompt, max_tokens=2500, temperature=0.1)
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            return json.loads(json_match.group()) if json_match else self._create_basic_feature_analysis(target_path)
        except Exception:
            return self._create_basic_feature_analysis(target_path)

    def _create_feature_flow_mermaid(self, analysis: Dict[str, Any]) -> str:
        lines = ["```mermaid", "sequenceDiagram", "    autonumber"]
        participants = set()
        
        for feature in analysis.get("features", []):
            for step in feature.get("flow_steps", []):
                participants.add(step.get("actor", "System"))
                participants.add(step.get("target", "System"))
                
        for actor in sorted(participants):
            lines.append(f"    participant {actor}")

        for feature in analysis.get("features", []):
            lines.append(f"\n    box LightBlue WorkFlow: {feature['name']}")
            lines.append(f"    Note over {list(participants)[0] if participants else 'System'}: {feature.get('description', '')}")
            lines.append("    end")
            for step in feature.get("flow_steps", []):
                actor = step.get("actor", "System")
                target = step.get("target", "System")
                action = step.get("action", "handles logic")
                lines.append(f"    {actor}->>+ {target}: {action}")
                lines.append(f"    {target}-->>- {actor}: Status Confirm")
        
        lines.append("```")
        return "\n".join(lines)
# ------------------------------------------------------------------ #
    #                     PROJECT CONCEPT VISUALIZER                     #
    # ------------------------------------------------------------------ #

    async def generate_project_concept(self, project_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        try:
            target_path = Path(project_path).resolve()
            concept = await self._analyze_project_concept_with_ai(target_path)
            mermaid_diagram = self._create_concept_mermaid(concept)
            markdown = self._format_concept_output(mermaid_diagram, concept, target_path)
            
            # Saves the .md file
            save_path = self._save_visualization(markdown, output_path, "project-concept") if output_path else None
            
            # --- NEW: GENERATES THE REAL PNG IMAGE ---
            png_path = None
            if save_path:
                png_path = save_mermaid_as_png(mermaid_diagram, save_path)
            # -----------------------------------------
            
            return {
                "success": True, 
                "diagram_type": "project_concept", 
                "markdown": markdown, 
                "mermaid": mermaid_diagram, 
                "saved_to": save_path,
                "image_saved_to": png_path,
                "components": len(concept.get("components", []))
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to generate project concept: {str(e)}"}

    async def _analyze_project_concept_with_ai(self, target_path: Path) -> Dict[str, Any]:
        context = self._gather_project_context(target_path)
        prompt = build_project_concept_prompt(
            project_name=target_path.name,
            structure=context["structure"]
        )
        response = await self.watsonx.generate_text(prompt=prompt, max_tokens=1500, temperature=0.2)
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            return json.loads(json_match.group()) if json_match else self._create_basic_concept(target_path)
        except Exception:
            return self._create_basic_concept(target_path)

    def _create_concept_mermaid(self, concept: Dict[str, Any]) -> str:
        lines = ["```mermaid", "graph LR"]
        lines.append("    classDef ui fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;")
        lines.append("    classDef server fill:#f3e8ff,stroke:#9333ea,stroke-width:2px;")
        lines.append("    classDef database fill:#dcfce7,stroke:#16a34a,stroke-width:2px;")
        
        for comp in concept.get("components", []):
            comp_id = comp["name"].replace(" ", "_")
            comp_type = comp.get("type", "component").lower()
            
            if "database" in comp_type:
                lines.append(f"    {comp_id}[({comp['name']})]\n    class {comp_id} database;")
            elif "ui" in comp_type:
                lines.append(f"    {comp_id}[/{comp['name']}/]\n    class {comp_id} ui;")
            else:
                lines.append(f"    {comp_id}[{comp['name']}]")
                if "server" in comp_type or "api" in comp_type:
                    lines.append(f"    class {comp_id} server;")
                    
            for target in comp.get("connects_to", []):
                lines.append(f"    {comp_id} --> {target.replace(' ', '_')}")
                
        for service in concept.get("external_services", []):
            lines.append(f"    ext_{service.replace(' ', '_')}{{{{{service}}}}}")
            
        lines.append("```")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #                       MARKDOWN FORMATTERS                          #
    # ------------------------------------------------------------------ #

    def _format_dependency_output(self, mermaid: str, dependencies: Dict[str, Any], target_path: Path) -> str:
        return f"# 📦 Dependency Chain Map\n**Root Directory:** `{target_path.name}`\n**Analysis Time:** {get_timestamp()}\n\n## System Architecture\n{mermaid}\n\n## Module Explanations\n" + "\n".join([f"- **{m}** maps out to source path location: `{p}`" for m, p in sorted(dependencies["modules"].items())])

    def _format_feature_flow_output(self, mermaid: str, analysis: Dict[str, Any], target_path: Path) -> str:
        md = f"# 🔄 Core Feature Flow Mappings\n**System Scope:** `{target_path.name}`\n**Generated Workflow:** {get_timestamp()}\n\n## Execution Sequence Map\n{mermaid}\n\n## Feature Specifications\n"
        for f in analysis.get("features", []):
            md += f"### Feature: {f.get('name', 'N/A')}\n- **Goal:** {f.get('description', 'N/A')}\n- **Entry Point:** `{f.get('entry_point', 'N/A')}`\n"
        return md

    def _format_concept_output(self, mermaid: str, concept: Dict[str, Any], target_path: Path) -> str:
        return f"# 🗺️ Structural Blueprint Concept\n**Project Platform:** `{target_path.name}`\n\n## Abstract Overview\n{concept.get('description', '')}\n\n## Concept Architecture Blueprint\n{mermaid}"

    def _gather_project_context(self, target_path: Path) -> Dict[str, str]:
        structure_lines = []
        key_files_content = {}
        for item in sorted(target_path.rglob("*")):
            if any(skip in item.parts for skip in ["__pycache__", "venv", ".venv", ".git", "node_modules"]): continue
            if item.is_file(): structure_lines.append(f"  {item.relative_to(target_path)}")
                
        for pattern in ["README.md", "main.py", "app.py", "server.py", "manage.py"]:
            for match in list(target_path.rglob(pattern))[:1]:
                content = self._get_file_content(str(match))
                if content: key_files_content[str(match.relative_to(target_path))] = content[:750]
                    
        return {"structure": "\n".join(structure_lines[:60]), "key_files": "\n\n".join([f"=== File: {k} ===\n{v}" for k, v in key_files_content.items()])}

    def _create_basic_feature_analysis(self, target_path: Path) -> Dict[str, Any]:
        return {"features": [{"name": "Default Init Core", "description": "Fallback automation module analysis", "entry_point": "main.py", "flow_steps": []}]}

    def _create_basic_concept(self, target_path: Path) -> Dict[str, Any]:
        return {"project_type": "Python application package", "description": "System architecture codebase", "components": [{"name": "AppCore", "type": "server", "description": "Primary internal services processor backend Layer", "connects_to": []}], "external_services": []}

    def _save_visualization(self, markdown: str, output_path: str, diagram_type: str) -> str:
        out = Path(output_path)
        if out.is_dir() or not out.suffix: out = out / f"{diagram_type}_{get_timestamp().replace(':', '-').replace(' ', '_')}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f: f.write(markdown)
        return str(out)
    
    import base64
    
import base64
import zlib
import urllib.request
from pathlib import Path

def save_mermaid_as_png(mermaid_code: str, base_output_path: str) -> str:
    """
    Converts Mermaid text directly into a real PNG image using the Kroki API.
    Requires NO local installations (no Graphviz, no Node.js).
    """
    try:
        # 1. Clean the markdown wrapper off the Mermaid string
        clean_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
        
        # 2. Compress and Base64 encode the string (Kroki's requirement)
        compressed = zlib.compress(clean_code.encode('utf-8'), 9)
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
        
        # 3. Build the API URL
        url = f"https://kroki.io/mermaid/png/{encoded}"
        
        # 4. Determine the final .png file path
        # If base_output_path is a .md file, change the extension to .png
        out_file = Path(base_output_path).with_suffix('.png')
        
        # 5. Download the image and save it to disk
        urllib.request.urlretrieve(url, str(out_file))
        
        return str(out_file)
        
    except Exception as e:
        return f"Error generating PNG: {str(e)}"